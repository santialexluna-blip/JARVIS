"""Núcleo unificado de JARVIS v2.0.

Centraliza conversación, sesiones, memoria persistente y búsqueda web.
Las acciones del sistema siguen pasando por herramientas explícitas.
"""

from .session_memory import SessionMemory
from .web_search import WebSearch


class JarvisCore:
    def __init__(self, ai, persistent_memory, tools, web_search=None, sessions=None):
        self.ai = ai
        self.persistent_memory = persistent_memory
        self.tools = tools
        self.web = web_search or WebSearch()
        self.sessions = sessions or SessionMemory()

    def handle(self, text: str, session_id: str = "default") -> str:
        text = text.strip()
        if not text:
            return "Necesito una instrucción."

        lower = text.lower()
        if lower in {"salir", "exit", "quit"}:
            return "__EXIT__"
        if lower in {"ayuda", "help"}:
            return (
                "Capacidades: conversación, memoria persistente, sesiones, hora, "
                "estado del sistema, búsqueda web y herramientas modulares."
            )

        if lower in {"hora", "qué hora es", "que hora es"}:
            return self.tools.call("time")
        if lower in {"sistema", "estado del sistema"}:
            return self.tools.call("system")

        if lower.startswith(("busca ", "buscar ")):
            query = text.split(" ", 1)[1].strip()
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

        if lower.startswith("recuerda "):
            note = text[8:].strip()
            if not note:
                return "Necesito saber qué quieres que recuerde."
            self.persistent_memory.add(note)
            return "He guardado esa nota en mi memoria local."

        if lower in {"mis notas", "notas", "memoria"}:
            notes = self.persistent_memory.list_all()
            return "No tengo notas guardadas." if not notes else "Tus notas: " + " | ".join(notes)

        messages = [
            {"role": "system", "content": "Eres JARVIS v2.0, un asistente personal útil, claro y seguro."}
        ]
        messages.extend(self.sessions.context(session_id, limit=10))
        messages.append({"role": "user", "content": text})
        answer = self.ai.reply(messages)
        self.sessions.add_message(session_id, "user", text)
        self.sessions.add_message(session_id, "assistant", answer)
        self.persistent_memory.add(f"Usuario: {text}")
        self.persistent_memory.add(f"JARVIS: {answer}")
        return answer
