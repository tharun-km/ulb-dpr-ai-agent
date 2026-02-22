"""
Selective information retrieval for context optimization.
"""
from typing import List, Dict, Any, Optional
from src.services.context_service.rag_service import rag_service
from src.services.context_service.token_budget import token_budget_manager


class SelectiveRetrieval:
    """
    Selective information retrieval system.
    Retrieves only relevant information to optimize context usage.
    """
    
    def __init__(self):
        self.rag_service = rag_service
        self.token_budget = token_budget_manager
    
    def retrieve_relevant_context(
        self,
        session_id: str,
        query: str,
        max_tokens: Optional[int] = None,
        sector: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context for a query, respecting token budget.
        """
        # Get remaining budget
        remaining = self.token_budget.get_remaining(session_id)
        if max_tokens:
            remaining = min(remaining, max_tokens)
        
        # Search for relevant documents
        results = self.rag_service.get_guidelines(query, sector)
        
        # Select documents that fit within budget
        selected = []
        tokens_used = 0
        
        for result in results:
            content = result.get("content", "")
            estimated_tokens = self.token_budget.estimate_tokens(content)
            
            if tokens_used + estimated_tokens <= remaining:
                selected.append(result)
                tokens_used += estimated_tokens
            else:
                break
        
        return {
            "documents": selected,
            "tokens_used": tokens_used,
            "tokens_remaining": remaining - tokens_used
        }
    
    def retrieve_compliance_requirements(
        self,
        session_id: str,
        sector: str,
        compliance_type: str = "general"
    ) -> List[Dict[str, Any]]:
        """Retrieve compliance requirements for a sector."""
        query = f"{compliance_type} compliance requirements {sector}"
        context = self.retrieve_relevant_context(session_id, query, sector=sector)
        return context.get("documents", [])
    
    def retrieve_financial_guidelines(
        self,
        session_id: str,
        sector: str
    ) -> List[Dict[str, Any]]:
        """Retrieve financial modeling guidelines for a sector."""
        query = f"financial modeling PPP {sector}"
        context = self.retrieve_relevant_context(session_id, query, sector=sector)
        return context.get("documents", [])
    
    def retrieve_risk_patterns(
        self,
        session_id: str,
        sector: str
    ) -> List[Dict[str, Any]]:
        """Retrieve historical risk patterns for a sector."""
        query = f"risk patterns failures {sector} PPP"
        context = self.retrieve_relevant_context(session_id, query, sector=sector)
        return context.get("documents", [])


# Global selective retrieval instance
selective_retrieval = SelectiveRetrieval()


