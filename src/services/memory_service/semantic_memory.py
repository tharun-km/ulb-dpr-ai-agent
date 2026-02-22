"""
Semantic memory for storing learned patterns about successful DPR structures.
"""
from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class DPRPattern(BaseModel):
    """A learned pattern about DPR structure."""
    pattern_id: str
    pattern_type: str  # e.g., "financial_structure", "compliance_checklist", "risk_mitigation"
    sector: str
    description: str
    key_elements: List[str]
    success_rate: float
    usage_count: int = 0


class SemanticMemory:
    """
    Semantic memory stores learned patterns about successful DPR structures.
    Helps agents apply proven patterns to new DPRs.
    """
    
    def __init__(self):
        self.patterns: Dict[str, DPRPattern] = {}
    
    def store_pattern(
        self,
        pattern_id: str,
        pattern_type: str,
        sector: str,
        description: str,
        key_elements: List[str],
        success_rate: float
    ) -> bool:
        """Store a learned pattern."""
        pattern = DPRPattern(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            sector=sector,
            description=description,
            key_elements=key_elements,
            success_rate=success_rate
        )
        self.patterns[pattern_id] = pattern
        return True
    
    def get_patterns(
        self,
        pattern_type: Optional[str] = None,
        sector: Optional[str] = None,
        min_success_rate: float = 0.0
    ) -> List[DPRPattern]:
        """Retrieve patterns matching criteria."""
        results = []
        
        for pattern in self.patterns.values():
            if pattern_type and pattern.pattern_type != pattern_type:
                continue
            if sector and pattern.sector != sector:
                continue
            if pattern.success_rate < min_success_rate:
                continue
            
            results.append(pattern)
        
        # Sort by success rate and usage count
        results.sort(key=lambda x: (x.success_rate, x.usage_count), reverse=True)
        return results
    
    def increment_usage(self, pattern_id: str) -> bool:
        """Increment usage count for a pattern."""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].usage_count += 1
            return True
        return False
    
    def update_success_rate(self, pattern_id: str, new_success_rate: float) -> bool:
        """Update success rate for a pattern."""
        if pattern_id in self.patterns:
            self.patterns[pattern_id].success_rate = new_success_rate
            return True
        return False
    
    def get_best_practices(self, sector: str, pattern_type: str) -> Optional[DPRPattern]:
        """Get the best practice pattern for a sector and type."""
        patterns = self.get_patterns(pattern_type=pattern_type, sector=sector, min_success_rate=0.7)
        if patterns:
            return patterns[0]
        return None


# Global semantic memory instance
semantic_memory = SemanticMemory()


