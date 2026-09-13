class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name, description, function):
        self._tools[name] = {"description": description, "function": function}

    def names(self):
        return list(self._tools)

    def call(self, name, *args, **kwargs):
        if name not in self._tools:
            raise KeyError(f"Herramienta desconocida: {name}")
        return self._tools[name]["function"](*args, **kwargs)
