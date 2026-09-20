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
