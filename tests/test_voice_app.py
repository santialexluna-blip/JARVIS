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
    assert conversation.process_text("Friday") == "Te escucho."
    assert conversation.process_text("cómo estás") == "respuesta"
    assistant.handle.assert_called_once_with("cómo estás", session_id="voice")


def test_clap_activates_and_greets():
    conversation, _assistant = build_conversation()
    assert conversation.process_text("__CLAP__") == "Hola. Te escucho."
    assert conversation.active is True


def test_stop_command_interrupts_speech():
    conversation, _assistant = build_conversation()
    conversation.voice.stop_speaking = Mock()
    assert conversation.process_text("silencio") is None
    conversation.voice.stop_speaking.assert_called_once_with()


def test_sleep_returns_to_standby():
    conversation, _ = build_conversation()
    conversation.process_text("Friday")
    assert "espera" in conversation.process_text("duerme")
    assert conversation.process_text("hola") is None


def test_voice_exit_stops_loop():
    conversation, _ = build_conversation()
    assert conversation.process_text("Friday salir") == "Hasta luego."
    assert conversation.running is False
