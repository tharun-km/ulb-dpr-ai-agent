"""
Base agent class for all agents in the multi-agent system.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import google.generativeai as genai
from src.utils.config import config
from src.services.observability.logging import agent_logger
from src.services.observability.metrics import metrics_collector
from src.services.context_service.token_budget import token_budget_manager


class BaseAgent(ABC):
    """
    Base class for all agents in the multi-agent system.
    Provides common functionality for agent initialization and execution.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.model = genai.GenerativeModel(
            model_name=config.agent_model,
            generation_config={
                "temperature": config.agent_temperature,
                "max_output_tokens": config.agent_max_tokens
            }
        )
        genai.configure(api_key=config.gemini_api_key)
    
    @abstractmethod
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            session_id: Session identifier
            input_data: Input data for the agent
            context: Optional context from previous agents
        
        Returns:
            Dictionary with agent output and results
        """
        pass
    
    def _generate_response(
        self,
        prompt: str,
        session_id: str,
        system_instruction: Optional[str] = None
    ) -> str:
        """Generate response using Gemini model."""
        try:
            # Track token usage
            estimated_input_tokens = token_budget_manager.estimate_tokens(prompt)
            token_budget_manager.track_usage(session_id, estimated_input_tokens)
            
            # Check budget
            if token_budget_manager.is_over_budget(session_id):
                raise ValueError(f"Token budget exceeded for session {session_id}")
            
            # Generate response
            if system_instruction:
                response = self.model.generate_content(
                    prompt,
                    generation_config={"system_instruction": system_instruction}
                )
            else:
                response = self.model.generate_content(prompt)
            
            # Track output tokens
            output_text = response.text
            estimated_output_tokens = token_budget_manager.estimate_tokens(output_text)
            token_budget_manager.track_usage(session_id, estimated_output_tokens)
            
            # Log token usage
            metrics_collector.record_token_usage(
                self.name,
                session_id,
                estimated_input_tokens + estimated_output_tokens
            )
            
            return output_text
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "generation_error",
                str(e),
                session_id
            )
            metrics_collector.record_error(self.name, "generation_error")
            raise
    
    def _log_decision(
        self,
        decision: str,
        rationale: str,
        confidence: float,
        session_id: str
    ) -> None:
        """Log agent decision."""
        agent_logger.log_agent_decision(
            self.name,
            decision,
            rationale,
            confidence,
            session_id
        )
    
    def _log_tool_call(
        self,
        tool_name: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        execution_time: float,
        session_id: str
    ) -> None:
        """Log tool call."""
        agent_logger.log_tool_call(
            self.name,
            tool_name,
            input_data,
            output_data,
            execution_time,
            session_id
        )


