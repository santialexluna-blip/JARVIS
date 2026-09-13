"""Núcleo unificado de JARVIS v2.0."""

from v1.4.web_search import WebSearch
from v1.5.memory import SessionMemory


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
        if lower.startswith(("busca ", "buscar ")):
            query = text.split(" ", 1)[1].strip()
            try:
                results = self.web.search(query, limit=5)
            except Exception as exc:
                return f"No pude completar la búsqueda web: {exc}"
            if not results:
                return "No encontré resultados para esa búsqueda."
            return "Resultados para: " + query + "\n" + "\n".join(
                f"{i}. {r.title} — {r.url}" for i, r in enumerate(results, 1)
            )

        messages = [{"role": "system", "content": "Eres JARVIS v2.0, un asistente personal útil, claro y seguro."}]
        messages.extend(self.sessions.context(session_id, limit=10))
        messages.append({"role": "user", "content": text})
        answer = self.ai.reply(messages)
        self.sessions.add_message(session_id, "user", text)
        self.sessions.add_message(session_id, "assistant", answer)
        self.persistent_memory.add(f"Usuario: {text}")
        self.persistent_memory.add(f"JARVIS: {answer}")
        return answer
