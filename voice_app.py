"""Conversación continua por voz para JARVIS."""

from assistant import Assistant
from voice import VoiceEngine


class VoiceConversation:
    def __init__(self, assistant=None, voice=None):
        self.assistant = assistant or Assistant()
        self.voice = voice or VoiceEngine(language="es-MX")
        self.active = False
        self.running = True

    def respond(self, message: str) -> None:
        print(f"JARVIS: {message}")
        self.voice.speak(message)

    def process_text(self, heard: str) -> str | None:
        if heard == "__CLAP__":
            self.active = True
            return "Hola. Te escucho."

        lowered_heard = heard.lower().strip(" ¿?¡!.,")
        if lowered_heard in {"para", "párate", "silencio", "cállate", "callate", "detente"}:
            self.voice.stop_speaking()
            return None

        command = VoiceEngine.strip_wake_word(heard)

        if command is not None:
            self.active = True
            if not command:
                return "Te escucho."
        elif self.active:
            command = heard.strip()
        else:
            return None

        lowered = command.lower().strip(" ¿?¡!.,")
        if lowered in {"duerme", "modo espera", "deja de escuchar"}:
            self.active = False
            return "De acuerdo. Quedo en espera. Di Friday para activarme."
        if lowered in {"salir", "apagate", "apágate", "cerrar"}:
            self.running = False
            return "Hasta luego."

        answer = self.assistant.handle(command, session_id="voice")
        if answer == "__EXIT__":
            self.running = False
            return "Hasta luego."
        return answer

    def run(self) -> int:
        print("JARVIS v2.2 — conversación por voz")
        print("Di 'Friday' para activarme. Di 'Friday, salir' para cerrar.")
        self.respond("Sistema de voz listo. Di Friday o aplaude para activarme.")

        while self.running:
            try:
                heard = self.voice.listen()
            except RuntimeError as exc:
                print(f"ERROR: {exc}")
                return 1
            except KeyboardInterrupt:
                self.respond("Hasta luego.")
                return 0

            if not heard:
                continue
            print(f"Tú: {heard}")
            response = self.process_text(heard)
            if response:
                self.respond(response)
        return 0


def main() -> int:
    return VoiceConversation().run()


if __name__ == "__main__":
    raise SystemExit(main())
