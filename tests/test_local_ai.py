import json
from unittest.mock import Mock, patch

from ai import HybridProvider, OllamaProvider


def test_ollama_provider_sends_conversation_to_local_api():
    response = Mock()
    response.status = 200
    response.read.return_value = json.dumps({
        "message": {"role": "assistant", "content": "Respuesta local"}
    }).encode("utf-8")
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)

    with patch("ai.urlopen", return_value=response) as mocked:
        answer = OllamaProvider().reply([{"role": "user", "content": "Hola"}])

    assert answer == "Respuesta local"
    request = mocked.call_args.args[0]
    payload = json.loads(request.data.decode("utf-8"))
    assert payload["model"] == "qwen3:4b"
    assert payload["stream"] is False
    assert payload["think"] is False
    assert mocked.call_args.kwargs["timeout"] == 25


def test_simple_greeting_does_not_wait_for_local_model():
    local = Mock()
    answer = HybridProvider(local=local).reply([{"role": "user", "content": "hola"}])
    assert "Soy Jarvis" in answer
    local.reply.assert_not_called()


def test_simple_calculation_does_not_wait_for_local_model():
    local = Mock()
    answer = HybridProvider(local=local).reply([{"role": "user", "content": "cuánto es 204 + 85 + 150"}])
    assert "439" in answer
    local.reply.assert_not_called()


def test_general_conversation_still_uses_local_model():
    local = Mock()
    local.reply.return_value = "Vamos a hablar de tu proyecto."
    messages = [{"role": "user", "content": "ayúdame con mi proyecto"}]
    assert HybridProvider(local=local).reply(messages) == "Vamos a hablar de tu proyecto."
    local.reply.assert_called_once_with(messages)


def test_slow_model_reports_timeout_instead_of_missing_installation():
    with patch.object(OllamaProvider, "ensure_available", return_value=True), \
         patch("ai.urlopen", side_effect=TimeoutError):
        answer = HybridProvider().reply([{"role": "user", "content": "explícame la física"}])
    assert "tardó demasiado" in answer
    assert "instalación" not in answer


def test_hybrid_provider_uses_basic_fallback_when_local_ai_is_offline():
    local = Mock()
    local.reply.side_effect = RuntimeError("offline")
    answer = HybridProvider(local=local).reply([{"role": "user", "content": "hola"}])
    assert "Soy Jarvis" in answer


def test_local_provider_starts_ollama_when_service_is_stopped():
    provider = OllamaProvider()
    with patch.object(provider, "available", side_effect=[False, False, True]), \
         patch.object(provider, "_find_ollama", return_value="ollama.exe"), \
         patch("ai.subprocess.Popen") as popen, \
         patch("ai.time.sleep"):
        assert provider.ensure_available(wait_seconds=2) is True
    popen.assert_called_once()
