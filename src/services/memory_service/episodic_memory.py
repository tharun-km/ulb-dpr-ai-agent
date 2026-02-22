"""
Episodic memory for storing past DPR creation attempts and outcomes.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class DPRAttempt(BaseModel):
    """Record of a past DPR creation attempt."""
    attempt_id: str
    ulb_name: str
    sector: str
    timestamp: str
    status: str
    outcome: Optional[str] = None
    lessons_learned: List[str] = []
    success_indicators: Dict[str, Any] = {}


class EpisodicMemory:
    """
    Episodic memory stores specific past DPR creation attempts.
    Helps agents learn from previous experiences.
    """
    
    def __init__(self):
        self.attempts: List[DPRAttempt] = []
    
    def store_attempt(
        self,
        attempt_id: str,
        ulb_name: str,
        sector: str,
        status: str,
        outcome: Optional[str] = None,
        lessons_learned: Optional[List[str]] = None,
        success_indicators: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store a DPR creation attempt."""
        attempt = DPRAttempt(
            attempt_id=attempt_id,
            ulb_name=ulb_name,
            sector=sector,
            timestamp=datetime.now().isoformat(),
            status=status,
            outcome=outcome,
            lessons_learned=lessons_learned or [],
            success_indicators=success_indicators or {}
        )
        self.attempts.append(attempt)
        return True
    
    def get_similar_attempts(
        self,
        ulb_name: Optional[str] = None,
        sector: Optional[str] = None,
        limit: int = 5
    ) -> List[DPRAttempt]:
        """Retrieve similar past attempts."""
        results = []
        
        for attempt in self.attempts:
            match = True
            if ulb_name and attempt.ulb_name != ulb_name:
                match = False
            if sector and attempt.sector != sector:
                match = False
            
            if match:
                results.append(attempt)
        
        # Sort by timestamp (most recent first)
        results.sort(key=lambda x: x.timestamp, reverse=True)
        return results[:limit]
    
    def get_successful_patterns(self, sector: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract patterns from successful attempts."""
        successful = [
            attempt for attempt in self.attempts
            if attempt.status == "completed" and attempt.outcome == "success"
        ]
        
        if sector:
            successful = [a for a in successful if a.sector == sector]
        
        patterns = []
        for attempt in successful:
            patterns.append({
                "ulb_name": attempt.ulb_name,
                "sector": attempt.sector,
                "success_indicators": attempt.success_indicators,
                "lessons_learned": attempt.lessons_learned
            })
        
        return patterns
    
    def get_failure_patterns(self, sector: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract patterns from failed attempts."""
        failed = [
            attempt for attempt in self.attempts
            if attempt.status == "failed" or attempt.outcome == "failure"
        ]
        
        if sector:
            failed = [a for a in failed if a.sector == sector]
        
        patterns = []
        for attempt in failed:
            patterns.append({
                "ulb_name": attempt.ulb_name,
                "sector": attempt.sector,
                "lessons_learned": attempt.lessons_learned,
                "failure_reasons": attempt.lessons_learned
            })
        
        return patterns


# Global episodic memory instance
episodic_memory = EpisodicMemory()


