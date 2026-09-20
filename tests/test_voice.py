from voice import VoiceEngine


def test_wake_word_is_required():
    assert VoiceEngine.strip_wake_word("hola") is None


def test_wake_word_alone_activates():
    assert VoiceEngine.strip_wake_word("JARVIS") == ""


def test_wake_word_extracts_command():
    assert VoiceEngine.strip_wake_word("JARVIS busca noticias") == "busca noticias"


def test_wake_word_accepts_natural_punctuation():
    assert VoiceEngine.strip_wake_word("Jarvis, busca noticias") == "busca noticias"
