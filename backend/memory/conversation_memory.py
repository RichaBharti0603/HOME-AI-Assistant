# Short-term in-memory conversation memory
# Maps session_id -> list of previous messages
from collections import deque
from typing import List, Dict

# Adjust max turns to keep in memory
MAX_MEMORY_TURNS = 6

conversation_memory: Dict[str, deque] = {}

def add_to_memory(session_id: str, role: str, text: str):
    """
    Add a message to conversation memory.
    role: 'user' or 'ai'
    """
    if session_id not in conversation_memory:
        conversation_memory[session_id] = deque(maxlen=MAX_MEMORY_TURNS)
    conversation_memory[session_id].append({"role": role, "text": text})

def get_memory(session_id: str) -> List[dict]:
    """
    Retrieve memory for a session as a list of dicts
    """
    return list(conversation_memory.get(session_id, []))

def clear_memory(session_id: str):
    """
    Clear memory for a session
    """
    if session_id in conversation_memory:
        del conversation_memory[session_id]
