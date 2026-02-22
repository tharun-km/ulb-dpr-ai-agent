"""
Aggregation potential evaluation for ULB clustering.
"""
from typing import Dict, Any, List
from src.models.dpr_schema import Sector, ULBCategory


class AggregationScorer:
    """
    Evaluates aggregation potential - ability to cluster ULBs for scale.
    """
    
    @staticmethod
    def evaluate_aggregation_potential(
        dpr_document: Dict[str, Any],
        similar_ulbs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate aggregation potential for a DPR.
        
        Args:
            dpr_document: The DPR document
            similar_ulbs: List of similar ULBs that could be clustered
        
        Returns:
            Dictionary with aggregation potential score and recommendations
        """
        source_ulb = dpr_document.get("ulb_metadata", {})
        source_category = source_ulb.get("category", "unknown")
        source_sector = dpr_document.get("sector", "unknown")
        
        # Count similar ULBs
        similar_count = len([
            ulb for ulb in similar_ulbs
            if ulb.get("category") == source_category
        ])
        
        # Check sector suitability for aggregation
        sector_suitability = AggregationScorer._check_sector_suitability(
            Sector(source_sector), source_category
        )
        
        # Calculate aggregation potential
        if similar_count >= 5:
            clustering_score = 1.0
        elif similar_count >= 3:
            clustering_score = 0.7
        elif similar_count >= 2:
            clustering_score = 0.5
        else:
            clustering_score = 0.2
        
        aggregation_score = (clustering_score * 0.6) + (sector_suitability * 0.4)
        
        return {
            "aggregation_score": aggregation_score,
            "clustering_score": clustering_score,
            "sector_suitability": sector_suitability,
            "similar_ulbs_count": similar_count,
            "aggregation_recommended": aggregation_score >= 0.6,
            "recommendations": AggregationScorer._get_recommendations(
                aggregation_score, similar_count, source_sector
            )
        }
    
    @staticmethod
    def _check_sector_suitability(sector: Sector, category: str) -> float:
        """Check if sector is suitable for aggregation in this category."""
        # Sectors with high aggregation potential
        high_aggregation_sectors = [Sector.SOLID_WASTE, Sector.STREETLIGHT]
        medium_aggregation_sectors = [Sector.WATER_SUPPLY]
        
        if sector in high_aggregation_sectors:
            return 1.0
        elif sector in medium_aggregation_sectors:
            return 0.7
        else:
            return 0.5
    
    @staticmethod
    def _get_recommendations(
        aggregation_score: float,
        similar_count: int,
        sector: str
    ) -> List[str]:
        """Get recommendations for aggregation."""
        recommendations = []
        
        if aggregation_score >= 0.6:
            recommendations.append(f"Consider aggregated PPP for {similar_count} similar ULBs")
            recommendations.append("Pool financial resources for better terms")
            recommendations.append("Share technical expertise across ULBs")
        
        if sector == "solid_waste":
            recommendations.append("Consider common processing facilities")
        elif sector == "water_supply":
            recommendations.append("Consider regional water supply schemes")
        
        return recommendations


