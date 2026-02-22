"""
Working memory for active context during current DPR creation session.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from src.models.dpr_schema import DPRDocument, DPRStatus


class WorkingMemory:
    """
    Working memory maintains active context during current session.
    Stores temporary data needed for current DPR creation process.
    """
    
    def __init__(self):
        self.active_contexts: Dict[str, Dict[str, Any]] = {}
    
    def initialize_context(self, session_id: str) -> bool:
        """Initialize working memory for a session."""
        self.active_contexts[session_id] = {
            "created_at": datetime.now().isoformat(),
            "current_step": None,
            "collected_data": {},
            "intermediate_results": {},
            "agent_decisions": [],
            "tool_calls": [],
            "errors": []
        }
        return True
    
    def update_current_step(self, session_id: str, step: str) -> bool:
        """Update current step in DPR creation process."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["current_step"] = step
        self.active_contexts[session_id]["updated_at"] = datetime.now().isoformat()
        return True
    
    def store_data(self, session_id: str, key: str, value: Any) -> bool:
        """Store data in working memory."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["collected_data"][key] = value
        self.active_contexts[session_id]["updated_at"] = datetime.now().isoformat()
        return True
    
    def get_data(self, session_id: str, key: Optional[str] = None) -> Optional[Any]:
        """Retrieve data from working memory."""
        if session_id not in self.active_contexts:
            return None
        
        if key:
            return self.active_contexts[session_id]["collected_data"].get(key)
        return self.active_contexts[session_id]["collected_data"]
    
    def store_intermediate_result(self, session_id: str, result_type: str, result: Any) -> bool:
        """Store intermediate result from agent processing."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["intermediate_results"][result_type] = result
        self.active_contexts[session_id]["updated_at"] = datetime.now().isoformat()
        return True
    
    def get_intermediate_result(self, session_id: str, result_type: str) -> Optional[Any]:
        """Retrieve intermediate result."""
        if session_id not in self.active_contexts:
            return None
        
        return self.active_contexts[session_id]["intermediate_results"].get(result_type)
    
    def log_agent_decision(self, session_id: str, agent_name: str, decision: str, rationale: str) -> bool:
        """Log an agent decision."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["agent_decisions"].append({
            "agent": agent_name,
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def log_tool_call(self, session_id: str, tool_name: str, input_data: Any, output_data: Any) -> bool:
        """Log a tool call."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["tool_calls"].append({
            "tool": tool_name,
            "input": input_data,
            "output": output_data,
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def log_error(self, session_id: str, error_type: str, error_message: str) -> bool:
        """Log an error."""
        if session_id not in self.active_contexts:
            self.initialize_context(session_id)
        
        self.active_contexts[session_id]["errors"].append({
            "type": error_type,
            "message": error_message,
            "timestamp": datetime.now().isoformat()
        })
        return True
    
    def clear_context(self, session_id: str) -> bool:
        """Clear working memory for a session."""
        if session_id in self.active_contexts:
            del self.active_contexts[session_id]
            return True
        return False
    
    def get_full_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get full working memory context for a session."""
        return self.active_contexts.get(session_id)


# Global working memory instance
working_memory = WorkingMemory()


