"""
Metrics collection for DPR quality, completion time, token usage, and costs.
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from prometheus_client import Counter, Histogram, Gauge
from src.utils.config import config


# Prometheus metrics
dpr_created_total = Counter(
    'dpr_created_total',
    'Total number of DPRs created',
    ['sector', 'ulb_category']
)

dpr_completion_time = Histogram(
    'dpr_completion_time_seconds',
    'Time taken to complete DPR creation',
    ['sector']
)

token_usage_total = Counter(
    'token_usage_total',
    'Total tokens used',
    ['agent', 'session_id']
)

agent_errors_total = Counter(
    'agent_errors_total',
    'Total agent errors',
    ['agent', 'error_type']
)

dpr_quality_score = Gauge(
    'dpr_quality_score',
    'DPR quality score',
    ['session_id', 'metric_type']
)


class MetricsCollector:
    """
    Collects metrics for agent performance and DPR quality.
    """
    
    def __init__(self):
        self.enabled = config.enable_metrics
    
    def record_dpr_created(self, sector: str, ulb_category: str) -> None:
        """Record DPR creation."""
        if self.enabled:
            dpr_created_total.labels(sector=sector, ulb_category=ulb_category).inc()
    
    def record_completion_time(self, sector: str, duration_seconds: float) -> None:
        """Record DPR completion time."""
        if self.enabled:
            dpr_completion_time.labels(sector=sector).observe(duration_seconds)
    
    def record_token_usage(self, agent: str, session_id: str, tokens: int) -> None:
        """Record token usage."""
        if self.enabled:
            token_usage_total.labels(agent=agent, session_id=session_id).inc(tokens)
    
    def record_error(self, agent: str, error_type: str) -> None:
        """Record agent error."""
        if self.enabled:
            agent_errors_total.labels(agent=agent, error_type=error_type).inc()
    
    def record_quality_score(
        self,
        session_id: str,
        metric_type: str,
        score: float
    ) -> None:
        """Record DPR quality score."""
        if self.enabled:
            dpr_quality_score.labels(
                session_id=session_id,
                metric_type=metric_type
            ).set(score)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        # This would typically query Prometheus or internal metrics store
        return {
            "dprs_created": "N/A",  # Would be actual count
            "average_completion_time": "N/A",
            "total_token_usage": "N/A",
            "error_rate": "N/A"
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()


