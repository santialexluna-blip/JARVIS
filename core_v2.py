"""Núcleo unificado de JARVIS v2.0.

Orquesta IA, memoria persistente, sesiones, búsqueda web y herramientas.
Las acciones del sistema deben seguir expuestas mediante herramientas explícitas.
"""

from typing import Optional

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

        self.sessions.add_message(session_id, "user", text)
        lower = text.lower()

        if lower.startswith("busca "):
            query = text[6:].strip()
            results = self.web.search(query)
            if not results:
                return "No encontré resultados."
            return self.web.format_results(results)

        messages = [{"role": "system", "content": "Eres JARVIS v2.0, un asistente personal útil, claro y seguro."}]
        for item in self.persistent_memory.context(limit=8):
            messages.append({"role": "user", "content": item})
        messages.extend(self.sessions.context(session_id, limit=10))
        answer = self.ai.reply(messages)
        self.sessions.add_message(session_id, "assistant", answer)
        self.persistent_memory.add(f"Usuario: {text}")
        self.persistent_memory.add(f"JARVIS: {answer}")
        return answer
