"""Capa de voz opcional para JARVIS v2.1.

La voz es desacoplada del núcleo: si las dependencias no están instaladas,
JARVIS sigue funcionando en modo texto.
"""

import threading
import audioop


class VoiceEngine:
    WAKE_WORD = "friday"
    WAKE_WORDS = ("friday", "fridai", "fraidei", "frayday")

    def __init__(self, language: str = "es-MX", preferred_voice_id: str | None = None,
                 profile: str = "spanish", microphone_index: int | None = None):
        self.language = language
        self.preferred_voice_id = preferred_voice_id
        self.profile = profile
        self.rate = 165 if profile == "cinematic" else 175
        self.volume = .96 if profile == "cinematic" else 1.0
        self.microphone_index = microphone_index
        self._recognizer = None
        self._tts = None
        self._tts_lock = threading.RLock()
        self._speaking = threading.Event()
        self._calibrated = False

    @property
    def available(self) -> bool:
        return self._recognizer is not None or self._tts is not None

    def setup_tts(self) -> bool:
        try:
            import pyttsx3
            self._tts = pyttsx3.init()
            voices = self._tts.getProperty("voices")
            voice_id = self.preferred_voice_id or self._best_voice_id(voices, self.profile)
            if voice_id:
                self._tts.setProperty("voice", voice_id)
            self._tts.setProperty("rate", self.rate)
            self._tts.setProperty("volume", self.volume)
            return True
        except Exception:
            self._tts = None
            return False

    @staticmethod
    def _best_voice_id(voices, profile: str = "spanish") -> str | None:
        """Elige el mejor timbre instalado para el perfil solicitado."""
        ranked = []
        for voice in voices or []:
            name = str(getattr(voice, "name", "")).lower()
            voice_id = str(getattr(voice, "id", ""))
            languages = " ".join(map(str, getattr(voice, "languages", []) or [])).lower()
            searchable = f"{name} {voice_id.lower()} {languages}"
            score = 0
            if profile == "cinematic":
                if any(token in searchable for token in ("george", "ryan", "mark", "en-gb", "en_gb", "british")):
                    score += 15
                if any(token in searchable for token in ("male", "mascul")):
                    score += 5
            else:
                if any(token in searchable for token in ("spanish", "español", "es-mx", "es_es", "es-")):
                    score += 10
                if any(token in searchable for token in ("pablo", "jorge", "david", "male", "mascul")):
                    score += 5
            ranked.append((score, voice_id))
        if not ranked:
            return None
        return max(ranked, key=lambda item: item[0])[1]

    def set_profile(self, profile: str, voice_id: str | None = None):
        self.profile = profile
        self.preferred_voice_id = voice_id
        self.rate = 165 if profile == "cinematic" else 175
        self.volume = .96 if profile == "cinematic" else 1.0
        self._tts = None

    def list_voices(self) -> list[dict[str, str]]:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            voices = [
                {"id": str(voice.id), "name": str(getattr(voice, "name", voice.id))}
                for voice in engine.getProperty("voices")
            ]
            engine.stop()
            return voices
        except Exception:
            return []

    def speak(self, text: str) -> bool:
        with self._tts_lock:
            if self._tts is None and not self.setup_tts():
                return False
            try:
                self._speaking.set()
                self._tts.say(text)
                self._tts.runAndWait()
                return True
            except Exception:
                return False
            finally:
                self._speaking.clear()
                # SAPI5 puede dejar el motor bloqueado después de la primera frase.
                # Liberarlo permite que cada respuesta use una sesión de voz limpia.
                try:
                    self._tts.stop()
                except Exception:
                    pass
                self._tts = None

    @property
    def speaking(self) -> bool:
        return self._speaking.is_set()

    def stop_speaking(self) -> None:
        """Interrumpe la frase actual sin esperar a que termine."""
        engine = self._tts
        if engine is not None:
            try:
                engine.stop()
            except Exception:
                pass
        self._speaking.clear()

    def setup_recognition(self) -> bool:
        try:
            import speech_recognition as sr

            self._recognizer = sr.Recognizer()
            self._recognizer.dynamic_energy_threshold = True
            return True
        except Exception:
            self._recognizer = None
            return False

    @staticmethod
    def list_microphones() -> list[str]:
        """Devuelve los micrófonos que PyAudio puede abrir en Windows."""
        try:
            import speech_recognition as sr
            return list(sr.Microphone.list_microphone_names())
        except Exception:
            return []

    def listen(self, timeout: int = 5, phrase_time_limit: int = 12) -> str | None:
        """Escucha una frase y la convierte a texto en español de México."""
        if self._recognizer is None and not self.setup_recognition():
            raise RuntimeError("El reconocimiento de voz no está disponible.")

        import speech_recognition as sr

        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                if not self._calibrated:
                    self._recognizer.adjust_for_ambient_noise(source, duration=0.6)
                    self._calibrated = True
                audio = self._recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
            raw = audio.get_raw_data(convert_width=2)
            if self._looks_like_clap(raw, 2):
                return "__CLAP__"
            return self._recognizer.recognize_google(audio, language=self.language).strip()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as exc:
            raise RuntimeError("No pude conectar con el reconocimiento de voz.") from exc
        except (OSError, AttributeError) as exc:
            raise RuntimeError(
                "Windows no me dio acceso al micrófono. Activa el permiso de micrófono "
                "para aplicaciones de escritorio y vuelve a abrir JARVIS."
            ) from exc

    @staticmethod
    def _looks_like_clap(raw_audio: bytes, sample_width: int = 2) -> bool:
        """Detecta un pico breve y fuerte, típico de un aplauso."""
        if not raw_audio:
            return False
        rms = audioop.rms(raw_audio, sample_width)
        peak = audioop.max(raw_audio, sample_width)
        return peak >= 12000 and rms >= 900 and peak >= rms * 2.4

    @staticmethod
    def strip_wake_word(text: str) -> str | None:
        normalized = text.strip()
        if not normalized:
            return None
        lowered = normalized.lower()
        for wake_word in VoiceEngine.WAKE_WORDS:
            if lowered == wake_word:
                return ""
            if lowered.startswith(wake_word):
                remainder = normalized[len(wake_word):]
                if remainder and (remainder[0].isspace() or remainder[0] in ",:;.-"):
                    return remainder.lstrip(" ,:;.-").strip()
        return None
