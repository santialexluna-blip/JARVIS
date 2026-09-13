from .router import Router
from .store import MemoryStore
from .basic import BasicTools
from .registry import ToolRegistry
from .ai import DemoProvider
from .web_search import WebSearch
from .session_memory import SessionMemory


class Assistant:
    def __init__(self):
        self.memory = MemoryStore()
        self.sessions = SessionMemory()
        self.basic = BasicTools()
        self.tools = ToolRegistry()
        self.tools.register("time", "Consulta la hora local.", self.basic.time)
        self.tools.register("system", "Consulta el estado del PC.", self.basic.system_info)
        self.web = WebSearch()
        self.ai = DemoProvider()
        self.router = Router(self.tools, self.memory, self.ai, self.web, self.sessions)

    def handle(self, text: str, session_id: str = "default") -> str:
        return self.router.route(text, session_id=session_id)
