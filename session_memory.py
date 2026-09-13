"""Memoria de conversación por sesiones para JARVIS v1.5."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Session:
    session_id: str
    messages: list[dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})


class SessionMemory:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        session_id = session_id.strip()
        if not session_id:
            raise ValueError("session_id no puede estar vacío")
        return self._sessions.setdefault(session_id, Session(session_id))

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.get_or_create(session_id).add(role, content)

    def context(self, session_id: str, limit: int = 10) -> list[dict[str, str]]:
        if limit < 1:
            return []
        return self.get_or_create(session_id).messages[-limit:]

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
