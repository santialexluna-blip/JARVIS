class Router:
    def __init__(self, tools, memory, ai):
        self.tools = tools
        self.memory = memory
        self.ai = ai

    def route(self, text: str) -> str:
        command = text.lower().strip()
        if command in {"salir", "exit", "quit"}:
            return "__EXIT__"
        if command in {"ayuda", "help"}:
            return "Capacidades: conversación, memoria, hora, estado del sistema y herramientas modulares."
        if command in {"hora", "qué hora es", "que hora es"}:
            return self.tools.call("time")
        if command in {"sistema", "estado del sistema"}:
            return self.tools.call("system")
        if command.startswith("recuerda "):
            note = text[8:].strip()
            if not note:
                return "Necesito saber qué quieres que recuerde."
            self.memory.add(note)
            return "He guardado esa nota en mi memoria local."
        if command in {"mis notas", "notas", "memoria"}:
            notes = self.memory.list_all()
            return "No tengo notas guardadas." if not notes else "Tus notas: " + " | ".join(notes)

        messages = [{"role": "system", "content": "Eres JARVIS, un asistente personal útil, claro y seguro."}]
        for item in self.memory.context():
            messages.append({"role": "user", "content": item})
        messages.append({"role": "user", "content": text})
        answer = self.ai.reply(messages)
        self.memory.add(f"Usuario: {text}")
        self.memory.add(f"JARVIS: {answer}")
        return answer
