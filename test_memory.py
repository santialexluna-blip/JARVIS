from pathlib import Path
from jarvis.memory.store import MemoryStore

def test_memory(tmp_path):
    store = MemoryStore(tmp_path / "data.json")
    store.add("prueba")
    assert store.list_all() == ["prueba"]
