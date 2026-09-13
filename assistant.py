from pathlib import Path
from .router import Router
from ..memory.store import MemoryStore
from ..tools.basic import BasicTools

class Assistant:
    def __init__(self):
        self.memory = MemoryStore(Path("jarvis/memory/data.json"))
        self.tools = BasicTools()
        self.router = Router(self.tools, self.memory)

    def handle(self, text: str) -> str:
        return self.router.route(text)
