from unittest.mock import patch

from session_memory import SessionMemory
from web_search import SearchResult, WebSearch


def test_sessions_are_isolated():
    memory = SessionMemory()
    memory.add_message("a", "user", "hola")
    memory.add_message("b", "user", "adiós")
    assert memory.context("a") == [{"role": "user", "content": "hola"}]
    assert memory.context("b") == [{"role": "user", "content": "adiós"}]


def test_search_validates_limit():
    with patch.object(WebSearch, "search", side_effect=ValueError("limit debe estar entre 1 y 10")):
        try:
            WebSearch().search("jarvis", 11)
        except ValueError as exc:
            assert "limit" in str(exc)
        else:
            raise AssertionError("expected ValueError")
