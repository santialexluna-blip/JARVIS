from memory import SessionMemory


def test_session_context_is_isolated():
    memory = SessionMemory()
    memory.add_message("a", "user", "hola")
    memory.add_message("b", "user", "adiós")
    assert memory.context("a") == [{"role": "user", "content": "hola"}]
    assert memory.context("b") == [{"role": "user", "content": "adiós"}]
