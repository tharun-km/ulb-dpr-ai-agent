"""
Agent-specific logging for decision points, tool selection, and confidence scores.
"""
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime
from src.utils.config import config


class AgentLogger:
    """
    Specialized logger for agent activities.
    Logs decisions, tool selections, and confidence scores.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("ulb_dpr_agent")
        self.logger.setLevel(getattr(logging, config.log_level))
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_agent_decision(
        self,
        agent_name: str,
        decision: str,
        rationale: str,
        confidence: float,
        session_id: Optional[str] = None
    ) -> None:
        """Log an agent decision with rationale and confidence."""
        log_data = {
            "type": "agent_decision",
            "agent": agent_name,
            "decision": decision,
            "rationale": rationale,
            "confidence": confidence,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"Agent Decision: {json.dumps(log_data)}")
    
    def log_tool_selection(
        self,
        agent_name: str,
        tool_name: str,
        selection_reason: str,
        session_id: Optional[str] = None
    ) -> None:
        """Log tool selection with reason."""
        log_data = {
            "type": "tool_selection",
            "agent": agent_name,
            "tool": tool_name,
            "reason": selection_reason,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"Tool Selection: {json.dumps(log_data)}")
    
    def log_tool_call(
        self,
        agent_name: str,
        tool_name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        execution_time: float,
        session_id: Optional[str] = None
    ) -> None:
        """Log tool call with input/output and execution time."""
        log_data = {
            "type": "tool_call",
            "agent": agent_name,
            "tool": tool_name,
            "input": input_data,
            "output": output_data,
            "execution_time": execution_time,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"Tool Call: {json.dumps(log_data)}")
    
    def log_error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        session_id: Optional[str] = None,
        traceback: Optional[str] = None
    ) -> None:
        """Log an error."""
        log_data = {
            "type": "error",
            "agent": agent_name,
            "error_type": error_type,
            "error_message": error_message,
            "session_id": session_id,
            "traceback": traceback,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.error(f"Error: {json.dumps(log_data)}")
    
    def log_status_change(
        self,
        session_id: str,
        old_status: str,
        new_status: str,
        reason: Optional[str] = None
    ) -> None:
        """Log status change."""
        log_data = {
            "type": "status_change",
            "session_id": session_id,
            "old_status": old_status,
            "new_status": new_status,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"Status Change: {json.dumps(log_data)}")


# Global agent logger instance
agent_logger = AgentLogger()


