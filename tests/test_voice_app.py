from unittest.mock import Mock

from voice_app import VoiceConversation


def build_conversation():
    assistant = Mock()
    assistant.handle.return_value = "respuesta"
    return VoiceConversation(assistant=assistant, voice=Mock()), assistant


def test_ignores_speech_until_wake_word():
    conversation, assistant = build_conversation()
    assert conversation.process_text("hola") is None
    assistant.handle.assert_not_called()


def test_wake_word_starts_continuous_conversation():
    conversation, assistant = build_conversation()
    assert conversation.process_text("Jarvis") == "Te escucho."
    assert conversation.process_text("cómo estás") == "respuesta"
    assistant.handle.assert_called_once_with("cómo estás", session_id="voice")


def test_sleep_returns_to_standby():
    conversation, _ = build_conversation()
    conversation.process_text("Jarvis")
    assert "espera" in conversation.process_text("duerme")
    assert conversation.process_text("hola") is None


def test_voice_exit_stops_loop():
    conversation, _ = build_conversation()
    assert conversation.process_text("Jarvis salir") == "Hasta luego."
    assert conversation.running is False
