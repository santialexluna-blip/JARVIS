class Router:
    def __init__(self, tools, memory):
        self.tools = tools
        self.memory = memory

    def route(self, text: str) -> str:
        command = text.lower().strip()

        if command in {"salir", "exit", "quit"}:
            return "__EXIT__"

        if command in {"ayuda", "help"}:
            return (
                "Puedo responder comandos básicos, consultar la hora, "
                "ver información del sistema, guardar notas y listarlas. "
                "La IA y la voz se añadirán como módulos independientes."
            )

        if command in {"hora", "qué hora es", "que hora es"}:
            return self.tools.time()

        if command in {"sistema", "estado del sistema"}:
            return self.tools.system_info()

        if command.startswith("recuerda "):
            note = text[8:].strip()
            if not note:
                return "Necesito saber qué quieres que recuerde."
            self.memory.add(note)
            return "He guardado esa nota en mi memoria local."

        if command in {"mis notas", "notas", "memoria"}:
            notes = self.memory.list_all()
            if not notes:
                return "No tengo notas guardadas."
            return "Tus notas: " + " | ".join(notes)

        return (
            "Entendido. Aún no tengo conectado el motor de IA, pero el núcleo "
            "está funcionando. Esta capa será conectada sin cambiar la arquitectura."
        )
