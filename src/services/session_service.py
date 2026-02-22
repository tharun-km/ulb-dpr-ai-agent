"""
Session management service using InMemorySessionService pattern.
"""
import time
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from src.models.dpr_schema import DPRStatus, DPRDocument
from src.utils.config import config


class InMemorySessionService:
    """
    In-memory session service for managing DPR creation sessions.
    Tracks progress across interactions within a session.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.timeout = config.session_timeout
    
    def create_session(self, session_id: str, initial_data: Optional[Dict[str, Any]] = None) -> str:
        """Create a new session."""
        self.sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "status": DPRStatus.INITIALIZED.value,
            "data": initial_data or {},
            "dpr_document": None,
            "context": {}
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data if it exists and hasn't timed out."""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        last_accessed = datetime.fromisoformat(session["last_accessed"])
        
        # Check timeout
        if datetime.now() - last_accessed > timedelta(seconds=self.timeout):
            self.delete_session(session_id)
            return None
        
        # Update last accessed
        session["last_accessed"] = datetime.now().isoformat()
        return session
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data."""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.update(updates)
        session["last_accessed"] = datetime.now().isoformat()
        return True
    
    def update_status(self, session_id: str, status: DPRStatus) -> bool:
        """Update DPR creation status."""
        return self.update_session(session_id, {"status": status.value})
    
    def store_dpr_document(self, session_id: str, dpr_document: DPRDocument) -> bool:
        """Store DPR document in session."""
        return self.update_session(session_id, {"dpr_document": dpr_document.model_dump()})
    
    def get_dpr_document(self, session_id: str) -> Optional[DPRDocument]:
        """Retrieve DPR document from session."""
        session = self.get_session(session_id)
        if not session or not session.get("dpr_document"):
            return None
        
        try:
            return DPRDocument(**session["dpr_document"])
        except Exception:
            return None
    
    def add_context(self, session_id: str, key: str, value: Any) -> bool:
        """Add context data to session."""
        session = self.get_session(session_id)
        if not session:
            return False
        
        if "context" not in session:
            session["context"] = {}
        
        session["context"][key] = value
        session["last_accessed"] = datetime.now().isoformat()
        return True
    
    def get_context(self, session_id: str, key: Optional[str] = None) -> Optional[Any]:
        """Get context data from session."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        context = session.get("context", {})
        if key:
            return context.get(key)
        return context
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions. Returns count of cleaned sessions."""
        now = datetime.now()
        expired = []
        
        for session_id, session in self.sessions.items():
            last_accessed = datetime.fromisoformat(session["last_accessed"])
            if now - last_accessed > timedelta(seconds=self.timeout):
                expired.append(session_id)
        
        for session_id in expired:
            self.delete_session(session_id)
        
        return len(expired)


# Global session service instance
session_service = InMemorySessionService()


