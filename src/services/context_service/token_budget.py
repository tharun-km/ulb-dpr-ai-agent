"""
Token budget management for large DPR documents.
"""
from typing import Dict, Optional
from src.utils.config import config


class TokenBudgetManager:
    """
    Manages token budget for context windows.
    Tracks token usage and provides warnings when approaching limits.
    """
    
    def __init__(self):
        self.max_tokens = config.max_context_tokens
        self.warning_threshold = config.token_budget_warning_threshold
        self.usage_tracking: Dict[str, int] = {}
    
    def get_budget(self) -> int:
        """Get maximum token budget."""
        return self.max_tokens
    
    def track_usage(self, session_id: str, tokens_used: int) -> None:
        """Track token usage for a session."""
        if session_id not in self.usage_tracking:
            self.usage_tracking[session_id] = 0
        self.usage_tracking[session_id] += tokens_used
    
    def get_usage(self, session_id: str) -> int:
        """Get current token usage for a session."""
        return self.usage_tracking.get(session_id, 0)
    
    def get_remaining(self, session_id: str) -> int:
        """Get remaining token budget for a session."""
        return max(0, self.max_tokens - self.get_usage(session_id))
    
    def get_usage_percentage(self, session_id: str) -> float:
        """Get token usage as percentage of budget."""
        if self.max_tokens == 0:
            return 0.0
        return min(1.0, self.get_usage(session_id) / self.max_tokens)
    
    def is_over_budget(self, session_id: str) -> bool:
        """Check if session has exceeded token budget."""
        return self.get_usage(session_id) > self.max_tokens
    
    def is_near_limit(self, session_id: str) -> bool:
        """Check if session is approaching token budget limit."""
        return self.get_usage_percentage(session_id) >= self.warning_threshold
    
    def reset_usage(self, session_id: str) -> None:
        """Reset token usage tracking for a session."""
        if session_id in self.usage_tracking:
            del self.usage_tracking[session_id]
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (rough approximation: 1 token ≈ 4 characters)."""
        return len(text) // 4


# Global token budget manager
token_budget_manager = TokenBudgetManager()


