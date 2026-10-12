from voice import VoiceEngine
from unittest.mock import Mock, patch
from types import SimpleNamespace
import struct

import pytest


def test_wake_word_is_required():
    assert VoiceEngine.strip_wake_word("hola") is None


def test_wake_word_alone_activates():
    assert VoiceEngine.strip_wake_word("KAREN") == ""


def test_wake_word_extracts_command():
    assert VoiceEngine.strip_wake_word("KAREN busca noticias") == "busca noticias"


def test_wake_word_accepts_natural_punctuation():
    assert VoiceEngine.strip_wake_word("Karen, busca noticias") == "busca noticias"


def test_wake_word_accepts_common_transcription_variants():
    assert VoiceEngine.strip_wake_word("Caren qué hora es") == "qué hora es"


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


def test_detects_a_short_clap_peak():
    quiet = (100).to_bytes(2, "little", signed=True) * 100
    peak = (20000).to_bytes(2, "little", signed=True)
    assert VoiceEngine._looks_like_clap(quiet + peak + quiet) is True


@pytest.mark.parametrize("heard,command", [
    ("¿Karen?", ""),
    ("Hola, Káren, qué hora es", "qué hora es"),
    ("Oye Caren busca noticias", "busca noticias"),
    ("Karín, recuerda mi tarea", "recuerda mi tarea"),
    ("Car en, hola", "hola"),
    ("karencita", None),
    ("me dijo Karen que sí", None),
])
def test_activation_with_transcription_variants_and_boundaries(heard, command):
    assert VoiceEngine.strip_wake_word(heard) == command


def test_loud_speech_with_separated_peaks_is_not_a_clap():
    # Cumple los límites de intensidad del detector anterior, pero contiene
    # dos sílabas fuertes separadas por 300 ms.
    samples = [100] * 8000
    samples[100:120] = [20000] * 20
    samples[4900:4920] = [20000] * 20
    audio = struct.pack("<" + "h" * len(samples), *samples)
    assert VoiceEngine._looks_like_clap(audio, sample_rate=16000) is False


def test_recognition_accepts_short_wake_word_and_bounds_network_wait():
    recognizer = SimpleNamespace()
    speech = SimpleNamespace(Recognizer=lambda: recognizer)
    with patch.dict("sys.modules", {"speech_recognition": speech}):
        assert VoiceEngine().setup_recognition() is True
    assert recognizer.phrase_threshold < 0.3
    assert recognizer.pause_threshold >= recognizer.non_speaking_duration
    assert recognizer.operation_timeout == 8
