"""Capa de voz opcional para JARVIS v2.1.

La voz es desacoplada del núcleo: si las dependencias no están instaladas,
JARVIS sigue funcionando en modo texto.
"""


class VoiceEngine:
    WAKE_WORD = "jarvis"

    def __init__(self, language: str = "es-MX"):
        self.language = language
        self._recognizer = None
        self._tts = None

    @property
    def available(self) -> bool:
        return self._recognizer is not None or self._tts is not None

    def setup_tts(self) -> bool:
        try:
            import pyttsx3
            self._tts = pyttsx3.init()
            return True
        except Exception:
            self._tts = None
            return False

    def speak(self, text: str) -> bool:
        if self._tts is None and not self.setup_tts():
            return False
        self._tts.say(text)
        self._tts.runAndWait()
        return True

    @staticmethod
    def strip_wake_word(text: str) -> str | None:
        normalized = text.strip()
        if not normalized:
            return None
        lowered = normalized.lower()
        if lowered == VoiceEngine.WAKE_WORD:
            return ""
        prefix = VoiceEngine.WAKE_WORD + " "
        if lowered.startswith(prefix):
            return normalized[len(prefix):].strip()
        return None
