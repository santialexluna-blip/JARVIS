from unittest.mock import Mock

from core_v2 import JarvisCore


def test_empty_input_is_rejected():
    core = JarvisCore(Mock(), Mock(), Mock())
    assert core.handle("   ") == "Necesito una instrucción."


def test_exit_command():
    core = JarvisCore(Mock(), Mock(), Mock())
    assert core.handle("salir") == "__EXIT__"


def test_help_command():
    core = JarvisCore(Mock(), Mock(), Mock())
    assert "búsqueda web" in core.handle("ayuda")


def test_time_uses_tool_registry():
    tools = Mock()
    tools.call.return_value = "15:00"
    core = JarvisCore(Mock(), Mock(), tools)
    assert core.handle("hora") == "15:00"
    tools.call.assert_called_once_with("time")


def test_session_context_is_sent_to_ai():
    ai = Mock()
    ai.reply.return_value = "respuesta"
    memory = Mock()
    sessions = Mock()
    sessions.context.return_value = [{"role": "user", "content": "hola"}]
    core = JarvisCore(ai, memory, Mock(), sessions=sessions)

    assert core.handle("¿cómo estás?", session_id="demo") == "respuesta"
    messages = ai.reply.call_args.args[0]
    assert messages[-2]["content"] == "hola"
    assert messages[-1]["content"] == "¿cómo estás?"
    sessions.add_message.assert_any_call("demo", "user", "¿cómo estás?")
    sessions.add_message.assert_any_call("demo", "assistant", "respuesta")
