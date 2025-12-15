# backend/memory/session_store.py

from typing import Dict, List

# In-memory session store
# session_id -> list of turns
_SESSIONS: Dict[str, List[Dict[str, str]]] = {}


def get_session(session_id: str) -> List[Dict[str, str]]:
    """
    Return conversation turns for a session.
    """
    return _SESSIONS.get(session_id, [])


def append_turn(session_id: str, role: str, content: str) -> None:
    """
    Append a user or assistant turn to a session.
    """
    if session_id not in _SESSIONS:
        _SESSIONS[session_id] = []

    _SESSIONS[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def get_summary(session_id: str, max_turns: int = 6) -> str:
    """
    Lightweight conversation summary.
    For Step 1, this simply returns the last N turns as context.
    """
    turns = _SESSIONS.get(session_id, [])

    if not turns:
        return ""

    recent = turns[-max_turns:]
    lines = []

    for t in recent:
        role = t["role"].capitalize()
        lines.append(f"{role}: {t['content']}")

    return "\n".join(lines)
