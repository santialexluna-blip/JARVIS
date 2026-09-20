"""Prueba sencilla de salida de voz para JARVIS en Windows."""

from voice import VoiceEngine


def main() -> int:
    voice = VoiceEngine(language="es-MX")
    message = "Hola, soy Jarvis. Mi sistema de voz funciona correctamente."

    print("Probando la voz de JARVIS...")
    if not voice.speak(message):
        print("No fue posible iniciar la voz. Revisa el audio de Windows.")
        return 1

    print("Prueba de voz completada correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
