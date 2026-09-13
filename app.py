from assistant import Assistant


def run():
    assistant = Assistant()
    print("JARVIS v2.1 — núcleo iniciado.")
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
        if response == "__EXIT__":
            print("JARVIS: Hasta luego.")
            break
        print(f"JARVIS: {response}")
