from .router import Router
from .store import MemoryStore
from .basic import BasicTools
from .registry import ToolRegistry
from .ai import DemoProvider

class Assistant:
    def __init__(self):
        self.memory = MemoryStore()
        self.basic = BasicTools()
        self.tools = ToolRegistry()
        self.tools.register("time", "Consulta la hora local.", self.basic.time)
        self.tools.register("system", "Consulta el estado del PC.", self.basic.system_info)
        self.ai = DemoProvider()
        self.router = Router(self.tools, self.memory, self.ai)

    def handle(self, text: str) -> str:
        return self.router.route(text)
