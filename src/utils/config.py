"""
Configuration management for the ULB DPR Assistant Agent.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class AgentConfig(BaseSettings):
    """Configuration for agent system."""
    
    # API Keys
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # Agent Configuration
    agent_model: str = Field(default="gemini-2.0-flash-exp", env="AGENT_MODEL")
    agent_temperature: float = Field(default=0.7, env="AGENT_TEMPERATURE")
    agent_max_tokens: int = Field(default=8192, env="AGENT_MAX_TOKENS")
    
    # Session and Memory
    session_timeout: int = Field(default=3600, env="SESSION_TIMEOUT")
    memory_bank_enabled: bool = Field(default=True, env="MEMORY_BANK_ENABLED")
    
    # Observability
    enable_logging: bool = Field(default=True, env="ENABLE_LOGGING")
    enable_tracing: bool = Field(default=True, env="ENABLE_TRACING")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Platform Integrations
    hudco_api_key: Optional[str] = Field(default=None, env="HUDCO_API_KEY")
    gati_shakti_api_key: Optional[str] = Field(default=None, env="GATI_SHAKTI_API_KEY")
    sebi_api_key: Optional[str] = Field(default=None, env="SEBI_API_KEY")
    mohua_api_key: Optional[str] = Field(default=None, env="MOHUA_API_KEY")
    
    # Token Budget Management
    max_context_tokens: int = Field(default=100000, env="MAX_CONTEXT_TOKENS")
    token_budget_warning_threshold: float = Field(default=0.8, env="TOKEN_BUDGET_WARNING_THRESHOLD")
    
    # State Configuration
    default_state: str = Field(default="chhattisgarh", env="DEFAULT_STATE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global configuration instance
config = AgentConfig()


