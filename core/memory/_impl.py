"""
Coreus Memory Manager (Reference Implementation)
------------------------------------------------
This module provides a functional interface for conversation history.

ARCHITECTURAL NOTE:
This reference implementation uses VOLATILE IN-MEMORY STORAGE (Python dict).
It is designed for stateless execution environments (like CI/CD or Demos).
Production environments utilize the Distributed Ledger engine for 
atomic persistence and vector-based semantic retrieval.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

class MemoryManager:
    """
    In-Memory conversation manager.
    """
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}

    def get_conversation(self, user_id: str) -> List[Dict[str, Any]]:
        if user_id not in self._storage:
            return []
        return self._storage[user_id].get("messages", [])

    def add_message(self, user_id: str, role: str, content: str) -> None:
        if user_id not in self._storage:
            self._storage[user_id] = {
                "created_at": datetime.now().isoformat(),
                "messages": []
            }
        
        message = {
            "id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self._storage[user_id]["messages"].append(message)
        print(f"[Memory] + {role.upper()}: {len(content)} chars")

    def clear(self, user_id: str) -> None:
        if user_id in self._storage:
            del self._storage[user_id]
