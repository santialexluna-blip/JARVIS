import json
from pathlib import Path
import os

class MemoryStore:
    def __init__(self, path=None):
        self.path = Path(path or os.getenv("JARVIS_MEMORY_PATH", "jarvis/memory/data.json"))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def _write(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, note: str):
        data = self._read()
        data.append(note)
        self._write(data)

    def list_all(self):
        return self._read()

    def context(self, limit=10):
        return self.list_all()[-limit:]
