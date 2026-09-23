from voice import VoiceEngine
from unittest.mock import Mock


def test_wake_word_is_required():
    assert VoiceEngine.strip_wake_word("hola") is None


def test_wake_word_alone_activates():
    assert VoiceEngine.strip_wake_word("JARVIS") == ""


def test_wake_word_extracts_command():
    assert VoiceEngine.strip_wake_word("JARVIS busca noticias") == "busca noticias"


def test_wake_word_accepts_natural_punctuation():
    assert VoiceEngine.strip_wake_word("Jarvis, busca noticias") == "busca noticias"


def test_wake_word_accepts_common_transcription_variants():
    assert VoiceEngine.strip_wake_word("Yarvis qué hora es") == "qué hora es"


def test_speech_engine_is_released_after_each_phrase():
    voice = VoiceEngine()
    engine = Mock()
    voice._tts = engine

    assert voice.speak("primera respuesta") is True
    engine.say.assert_called_once_with("primera respuesta")
    engine.runAndWait.assert_called_once_with()
    engine.stop.assert_called_once_with()
    assert voice._tts is None


def test_prefers_masculine_spanish_voice():
    spanish = Mock(id="spanish-pablo", name="Microsoft Pablo", languages=["es-MX"])
    english = Mock(id="english-zira", name="Microsoft Zira", languages=["en-US"])
    assert VoiceEngine._best_voice_id([english, spanish]) == "spanish-pablo"


def test_cinematic_profile_prefers_british_masculine_voice():
    english = type("Voice", (), {"name": "Microsoft George", "id": "en-gb-george", "languages": ["en-GB"]})()
    spanish = type("Voice", (), {"name": "Microsoft Pablo", "id": "spanish-pablo", "languages": ["es-MX"]})()
    assert VoiceEngine._best_voice_id([spanish, english], "cinematic") == "en-gb-george"


def test_microphone_index_can_be_selected():
    voice = VoiceEngine(microphone_index=2)
    assert voice.microphone_index == 2
