"""
In-memory session store for maintaining conversation history across requests.
Each session stores a list of ChatMessage objects representing the full conversation.
"""
import uuid
from typing import Dict, List, Optional

from models.schemas import ChatMessage


class SessionStore:
    """
    Thread-safe in-memory store for chat sessions.
    Each session maintains its own conversation history.
    """

    def __init__(self):
        # Dictionary mapping session_id -> List[ChatMessage]
        self._sessions: Dict[str, List[ChatMessage]] = {}

    def create_session(self) -> str:
        """
        Create a new chat session and return its ID.
        
        Returns:
            New session ID (UUID string)
        """
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = []
        return session_id

    def get_history(self, session_id: str) -> Optional[List[ChatMessage]]:
        """
        Retrieve conversation history for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of ChatMessage objects, or None if session doesn't exist
        """
        return self._sessions.get(session_id)

    def add_message(self, session_id: str, message: ChatMessage) -> None:
        """
        Add a message to the session's conversation history.
        
        Args:
            session_id: Session identifier
            message: ChatMessage to add
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        
        # Limit history to last 50 messages to prevent memory issues
        self._sessions[session_id].append(message)
        if len(self._sessions[session_id]) > 50:
            self._sessions[session_id] = self._sessions[session_id][-50:]

    def update_history(self, session_id: str, history: List[ChatMessage]) -> None:
        """
        Replace the entire history for a session.
        
        Args:
            session_id: Session identifier
            history: New conversation history
        """
        self._sessions[session_id] = history[-50:]  # Keep last 50 messages

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session exists, False otherwise
        """
        return session_id in self._sessions


# Global singleton instance
_session_store = SessionStore()


def get_session_store() -> SessionStore:
    """Get the global session store instance."""
    return _session_store
