"""Punto de entrada de las funciones nuevas de JARVIS v2.1."""

from .assistant import Assistant
from .hud import JarvisHUD
from .voice import VoiceEngine


def run_hud():
    assistant = Assistant()
    hud = JarvisHUD()
    hud.set_handler(assistant.handle)
    hud.run()


def run_voice_demo(text: str) -> str:
    """Procesa texto como si viniera de voz y exige la palabra de activación."""
    command = VoiceEngine.strip_wake_word(text)
    if command is None:
        return "Di 'JARVIS' seguido de una instrucción."
    if not command:
        return "JARVIS activo. ¿En qué puedo ayudarte?"
    return Assistant().handle(command)
