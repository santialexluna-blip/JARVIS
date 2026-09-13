from basic import BasicTools
from core_v2 import JarvisCore
from registry import ToolRegistry
from session_memory import SessionMemory
from store import MemoryStore
from web_search import WebSearch
from ai import DemoProvider


class Assistant:
    """Punto de entrada de JARVIS v2.1."""

    def __init__(self):
        self.memory = MemoryStore()
        self.sessions = SessionMemory()
        self.basic = BasicTools()
        self.tools = ToolRegistry()
        self.tools.register("time", "Consulta la hora local.", self.basic.time)
        self.tools.register("system", "Consulta el estado del PC.", self.basic.system_info)
        self.web = WebSearch()
        self.ai = DemoProvider()
        self.core = JarvisCore(
            ai=self.ai,
            persistent_memory=self.memory,
            tools=self.tools,
            web_search=self.web,
            sessions=self.sessions,
        )

    def handle(self, text: str, session_id: str = "default") -> str:
        return self.core.handle(text, session_id=session_id)
