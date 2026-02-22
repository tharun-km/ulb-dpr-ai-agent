"""
Replicability index for measuring DPR adaptability across ULBs.
"""
from typing import Dict, Any, List
from src.models.dpr_schema import ULBCategory, Sector


class ReplicabilityScorer:
    """
    Scores DPR replicability - how well it can be adapted to similar ULBs.
    """
    
    @staticmethod
    def calculate_replicability_index(
        dpr_document: Dict[str, Any],
        target_ulbs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate replicability index for a DPR.
        
        Args:
            dpr_document: The DPR document
            target_ulbs: List of target ULBs for replication
        
        Returns:
            Dictionary with replicability score and analysis
        """
        source_ulb = dpr_document.get("ulb_metadata", {})
        source_category = source_ulb.get("category", "unknown")
        source_sector = dpr_document.get("sector", "unknown")
        
        # Count compatible ULBs
        compatible_ulbs = []
        for ulb in target_ulbs:
            if ulb.get("category") == source_category:
                compatible_ulbs.append(ulb)
        
        compatibility_score = len(compatible_ulbs) / len(target_ulbs) if target_ulbs else 0.0
        
        # Check template quality
        template_score = ReplicabilityScorer._assess_template_quality(dpr_document)
        
        # Calculate overall replicability
        replicability_score = (compatibility_score * 0.6) + (template_score * 0.4)
        
        return {
            "replicability_score": replicability_score,
            "compatibility_score": compatibility_score,
            "template_score": template_score,
            "compatible_ulbs_count": len(compatible_ulbs),
            "total_target_ulbs": len(target_ulbs),
            "replicable": replicability_score >= 0.7,
            "recommendations": ReplicabilityScorer._get_recommendations(
                replicability_score, compatibility_score, template_score
            )
        }
    
    @staticmethod
    def _assess_template_quality(dpr_document: Dict[str, Any]) -> float:
        """Assess how well-structured the DPR is as a template."""
        required_sections = [
            "executive_summary",
            "project_description",
            "technical_specifications",
            "financial_model",
            "implementation_plan"
        ]
        
        present_sections = sum(
            1 for section in required_sections
            if section in dpr_document
        )
        
        return present_sections / len(required_sections) if required_sections else 0.0
    
    @staticmethod
    def _get_recommendations(
        replicability_score: float,
        compatibility_score: float,
        template_score: float
    ) -> List[str]:
        """Get recommendations to improve replicability."""
        recommendations = []
        
        if replicability_score < 0.7:
            if compatibility_score < 0.5:
                recommendations.append("Consider adapting for multiple ULB categories")
            
            if template_score < 0.7:
                recommendations.append("Improve DPR structure and completeness")
                recommendations.append("Ensure all required sections are present")
        
        recommendations.append("Document adaptation guidelines for different ULB sizes")
        
        return recommendations


