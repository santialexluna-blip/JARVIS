class Router:
    def __init__(self, tools, memory, ai, web=None, sessions=None):
        self.tools = tools
        self.memory = memory
        self.ai = ai
        self.web = web
        self.sessions = sessions

    def route(self, text: str, session_id: str = "default") -> str:
        command = text.lower().strip()
        if command in {"salir", "exit", "quit"}:
            return "__EXIT__"
        if command in {"ayuda", "help"}:
            return ("Capacidades: conversación, memoria persistente, sesiones, hora, "
                    "estado del sistema, búsqueda web y herramientas modulares.")
        if command in {"hora", "qué hora es", "que hora es"}:
            return self.tools.call("time")
        if command in {"sistema", "estado del sistema"}:
            return self.tools.call("system")

        if command.startswith("busca ") or command.startswith("buscar "):
            query = text.split(" ", 1)[1].strip()
            if not self.web:
                return "La búsqueda web no está configurada."
            try:
                results = self.web.search(query, limit=5)
            except Exception as exc:
                return f"No pude completar la búsqueda web: {exc}"
            if not results:
                return "No encontré resultados para esa búsqueda."
            lines = [f"Resultados para: {query}"]
            for index, result in enumerate(results, 1):
                snippet = f" — {result.snippet}" if result.snippet else ""
                lines.append(f"{index}. {result.title}{snippet}\n{result.url}")
            return "\n".join(lines)

        if command.startswith("recuerda "):
            note = text[8:].strip()
            if not note:
                return "Necesito saber qué quieres que recuerde."
            self.memory.add(note)
            return "He guardado esa nota en mi memoria local."
        if command in {"mis notas", "notas", "memoria"}:
            notes = self.memory.list_all()
            return "No tengo notas guardadas." if not notes else "Tus notas: " + " | ".join(notes)

        if self.sessions:
            messages = [{"role": "system", "content": "Eres JARVIS, un asistente personal útil, claro y seguro."}]
            messages.extend(self.sessions.context(session_id, limit=10))
        else:
            messages = [{"role": "system", "content": "Eres JARVIS, un asistente personal útil, claro y seguro."}]
            messages.extend({"role": "user", "content": item} for item in self.memory.context())
        messages.append({"role": "user", "content": text})
        answer = self.ai.reply(messages)

        if self.sessions:
            self.sessions.add_message(session_id, "user", text)
            self.sessions.add_message(session_id, "assistant", answer)
        self.memory.add(f"Usuario: {text}")
        self.memory.add(f"JARVIS: {answer}")
        return answer
