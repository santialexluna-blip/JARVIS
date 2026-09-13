"""Memoria avanzada de sesiones para JARVIS v1.5."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class Session:
    session_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})


class SessionMemory:
    """Gestiona sesiones aisladas y su contexto reciente."""

    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if not session_id.strip():
            raise ValueError("session_id no puede estar vacío")
        return self._sessions.setdefault(session_id, Session(session_id=session_id))

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.get_or_create(session_id).add(role, content)

    def context(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        if limit < 1:
            return []
        return self.get_or_create(session_id).messages[-limit:]

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
