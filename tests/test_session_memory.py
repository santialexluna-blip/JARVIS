from session_memory import SessionMemory


def test_sessions_are_isolated():
    memory = SessionMemory()
    memory.add_message("a", "user", "hola")
    memory.add_message("b", "user", "adiós")
    assert memory.context("a") == [{"role": "user", "content": "hola"}]
    assert memory.context("b") == [{"role": "user", "content": "adiós"}]


def test_clear_removes_only_selected_session():
    memory = SessionMemory()
    memory.add_message("a", "user", "hola")
    memory.add_message("b", "user", "adiós")
    memory.clear("a")
    assert memory.context("a") == []
    assert memory.context("b") == [{"role": "user", "content": "adiós"}]
