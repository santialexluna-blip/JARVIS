from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def reply(self, messages):
        raise NotImplementedError

class DemoProvider(AIProvider):
    def reply(self, messages):
        last = messages[-1]["content"] if messages else ""
        return f"He recibido: {last}. El motor de IA está preparado para conectarse."
