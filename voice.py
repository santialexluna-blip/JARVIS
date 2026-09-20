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
        self._calibrated = False

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
        try:
            self._tts.say(text)
            self._tts.runAndWait()
            return True
        except Exception:
            return False
        finally:
            # SAPI5 puede dejar el motor bloqueado después de la primera frase.
            # Liberarlo permite que cada respuesta use una sesión de voz limpia.
            try:
                self._tts.stop()
            except Exception:
                pass
            self._tts = None

    def setup_recognition(self) -> bool:
        try:
            import speech_recognition as sr

            self._recognizer = sr.Recognizer()
            self._recognizer.dynamic_energy_threshold = True
            return True
        except Exception:
            self._recognizer = None
            return False

    def listen(self, timeout: int = 5, phrase_time_limit: int = 12) -> str | None:
        """Escucha una frase y la convierte a texto en español de México."""
        if self._recognizer is None and not self.setup_recognition():
            raise RuntimeError("El reconocimiento de voz no está disponible.")

        import speech_recognition as sr

        try:
            with sr.Microphone() as source:
                if not self._calibrated:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.6)
                    self._calibrated = True
                audio = self._recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
            return self._recognizer.recognize_google(audio, language=self.language).strip()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as exc:
            raise RuntimeError("No pude conectar con el reconocimiento de voz.") from exc

    @staticmethod
    def strip_wake_word(text: str) -> str | None:
        normalized = text.strip()
        if not normalized:
            return None
        lowered = normalized.lower()
        if lowered == VoiceEngine.WAKE_WORD:
            return ""
        if lowered.startswith(VoiceEngine.WAKE_WORD):
            remainder = normalized[len(VoiceEngine.WAKE_WORD):]
            if remainder and (remainder[0].isspace() or remainder[0] in ",:;.-"):
                return remainder.lstrip(" ,:;.-").strip()
        return None
