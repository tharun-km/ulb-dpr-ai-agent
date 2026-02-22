"""
Aggregation intelligence for ULB clustering and sector-wise pooling recommendations.
"""
from typing import List, Dict, Any
from src.models.dpr_schema import ULBCategory, Sector


class AggregationIntelligence:
    """
    Identifies clustering opportunities across ULBs.
    Recommends sector-wise pooling for scale optimization.
    """
    
    @staticmethod
    def identify_clustering_opportunities(
        ulbs: List[Dict[str, Any]],
        sector: Sector,
        min_cluster_size: int = 3
    ) -> Dict[str, Any]:
        """
        Identify ULBs that can be clustered for aggregated PPPs.
        """
        # Group by category and proximity
        clusters = []
        
        # Group by category
        by_category = {}
        for ulb in ulbs:
            category = ulb.get("category", "unknown")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(ulb)
        
        # Create clusters from categories
        for category, category_ulbs in by_category.items():
            if len(category_ulbs) >= min_cluster_size:
                clusters.append({
                    "cluster_id": f"{category}_{sector.value}",
                    "category": category,
                    "sector": sector.value,
                    "ulbs": category_ulbs,
                    "total_population": sum(ulb.get("population", 0) for ulb in category_ulbs),
                    "aggregation_benefits": AggregationIntelligence._calculate_benefits(
                        category_ulbs, sector
                    )
                })
        
        return {
            "clusters": clusters,
            "total_clusters": len(clusters),
            "recommendations": AggregationIntelligence._get_clustering_recommendations(clusters)
        }
    
    @staticmethod
    def _calculate_benefits(ulbs: List[Dict[str, Any]], sector: Sector) -> Dict[str, Any]:
        """Calculate benefits of aggregating ULBs."""
        total_population = sum(ulb.get("population", 0) for ulb in ulbs)
        
        benefits = {
            "scale_economies": "high" if total_population > 200000 else "medium",
            "investor_attractiveness": "high" if len(ulbs) >= 5 else "medium",
            "cost_sharing": True,
            "risk_distribution": True
        }
        
        return benefits
    
    @staticmethod
    def _get_clustering_recommendations(clusters: List[Dict[str, Any]]) -> List[str]:
        """Get recommendations for clustering."""
        recommendations = []
        
        if len(clusters) > 0:
            recommendations.append("Consider aggregated PPP for clustered ULBs")
            recommendations.append("Pool financial resources for better terms")
            recommendations.append("Share technical expertise across ULBs")
        
        return recommendations
    
    @staticmethod
    def recommend_sector_pooling(
        sector: Sector,
        ulb_categories: List[ULBCategory]
    ) -> Dict[str, Any]:
        """
        Recommend sector-wise pooling strategies.
        """
        pooling_strategies = {
            Sector.WATER_SUPPLY: {
                "recommended": ["class_ii", "class_iii"],
                "approach": "Regional water supply schemes",
                "benefits": [
                    "Shared treatment facilities",
                    "Bulk water procurement",
                    "Cost optimization"
                ]
            },
            Sector.SOLID_WASTE: {
                "recommended": ["class_ii", "class_iii", "nagar_panchayat"],
                "approach": "Common processing facilities",
                "benefits": [
                    "Shared waste processing plants",
                    "Transportation optimization",
                    "Technology sharing"
                ]
            },
            Sector.URBAN_TRANSPORT: {
                "recommended": ["class_i", "class_ii"],
                "approach": "Regional transport networks",
                "benefits": [
                    "Inter-city connectivity",
                    "Shared fleet management",
                    "Integrated ticketing"
                ]
            },
            Sector.STREETLIGHT: {
                "recommended": ["class_iii", "nagar_panchayat"],
                "approach": "Bulk procurement and maintenance",
                "benefits": [
                    "Economies of scale",
                    "Shared maintenance teams",
                    "Technology standardization"
                ]
            }
        }
        
        strategy = pooling_strategies.get(sector, {})
        
        return {
            "sector": sector.value,
            "recommended_categories": strategy.get("recommended", []),
            "approach": strategy.get("approach", ""),
            "benefits": strategy.get("benefits", []),
            "applicable_ulbs": [
                cat.value for cat in ulb_categories
                if cat.value in strategy.get("recommended", [])
            ]
        }


