"""In-memory conversation memory implementation (no database)."""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from langchain_core.messages import BaseMessage


class InMemoryConversationMemory:
    """In-memory conversation memory for multi-turn conversations."""

    def __init__(self, max_conversation_age_hours: int = 24):
        self.max_conversation_age_hours = max_conversation_age_hours
        self.conversation_metadata: Dict[str, Dict[str, Any]] = {}
        self.conversation_messages: Dict[str, List[BaseMessage]] = {}

    def get_or_create_conversation_id(
        self, user_id: str, provided_conversation_id: Optional[str] = None
    ) -> str:
        if provided_conversation_id and provided_conversation_id in self.conversation_metadata:
            meta = self.conversation_metadata[provided_conversation_id]
            if meta.get("user_id") == user_id and meta.get("is_active", True):
                meta["last_accessed"] = datetime.utcnow()
                return provided_conversation_id

        conversation_id = str(uuid.uuid4())
        self.conversation_metadata[conversation_id] = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow(),
            "message_count": 0,
            "is_active": True,
        }
        self.conversation_messages[conversation_id] = []
        return conversation_id

    def add_message(self, conversation_id: str, message: BaseMessage) -> None:
        if conversation_id not in self.conversation_messages:
            self.conversation_messages[conversation_id] = []
            self.conversation_metadata[conversation_id] = {
                "user_id": "unknown",
                "created_at": datetime.utcnow(),
                "last_accessed": datetime.utcnow(),
                "message_count": 0,
                "is_active": True,
            }
        self.conversation_messages[conversation_id].append(message)
        meta = self.conversation_metadata.get(conversation_id, {})
        meta["last_accessed"] = datetime.utcnow()
        meta["message_count"] = int(meta.get("message_count", 0)) + 1
        self.conversation_metadata[conversation_id] = meta

    def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[BaseMessage]:
        meta = self.conversation_metadata.get(conversation_id)
        if meta:
            meta["last_accessed"] = datetime.utcnow()
        messages = self.conversation_messages.get(conversation_id, [])
        return messages[-limit:]

    def cleanup_old_conversations(self) -> int:
        cutoff_time = datetime.utcnow() - timedelta(hours=self.max_conversation_age_hours)
        cleaned = 0
        for cid, meta in list(self.conversation_metadata.items()):
            if meta.get("last_accessed", datetime.utcnow()) < cutoff_time and meta.get("is_active", True):
                meta["is_active"] = False
                cleaned += 1
        return cleaned

    def get_conversation_stats(self) -> Dict[str, Any]:
        active = [m for m in self.conversation_metadata.values() if m.get("is_active", True)]
        total_messages = sum(int(m.get("message_count", 0)) for m in self.conversation_metadata.values())
        oldest = min((m.get("created_at") for m in active), default=None)
        newest = max((m.get("created_at") for m in active), default=None)
        return {
            "total_conversations": len(active),
            "total_messages": total_messages,
            "oldest_conversation": oldest,
            "newest_conversation": newest,
        }

    def delete_conversation(self, conversation_id: str) -> bool:
        existed = conversation_id in self.conversation_metadata
        self.conversation_metadata.pop(conversation_id, None)
        self.conversation_messages.pop(conversation_id, None)
        return existed


# Global conversation memory instance
_conversation_memory: Optional[InMemoryConversationMemory] = None


def get_conversation_memory() -> InMemoryConversationMemory:
    """Get the global conversation memory instance."""
    global _conversation_memory
    if _conversation_memory is None:
        _conversation_memory = InMemoryConversationMemory()
    return _conversation_memory
