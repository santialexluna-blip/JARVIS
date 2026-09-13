from .core.assistant import Assistant

def run():
    assistant = Assistant()
    print("JARVIS v1.0 — listo.")
    print("Escribe 'ayuda' para ver capacidades o 'salir' para terminar.")
    while True:
        try:
            text = input("\nTú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nJARVIS: Hasta luego.")
            break
        if not text:
            continue
        response = assistant.handle(text)
        print(f"JARVIS: {response}")
        if response == "__EXIT__":
            break
