"""
ULB size-based categories and their PPP approach recommendations.
"""
from typing import Dict, List
from src.models.dpr_schema import ULBCategory, Sector


class ULBCategoryConfig:
    """Configuration for different ULB categories."""
    
    # PPP approach recommendations by category
    PPP_APPROACHES: Dict[ULBCategory, List[str]] = {
        ULBCategory.CLASS_I: [
            "Full PPP potential",
            "Direct private investment",
            "Municipal bonds eligible",
            "Large-scale infrastructure projects"
        ],
        ULBCategory.CLASS_II: [
            "Aggregated PPPs",
            "Pooled financing",
            "Regional partnerships",
            "Medium-scale projects"
        ],
        ULBCategory.CLASS_III: [
            "Service contracts",
            "O&M contracts",
            "Limited PPP scope",
            "Small-scale projects"
        ],
        ULBCategory.NAGAR_PANCHAYAT: [
            "Joint ventures only",
            "Community-based models",
            "Government grants primary",
            "Minimal private participation"
        ]
    }
    
    # Sector suitability by category
    SECTOR_SUITABILITY: Dict[ULBCategory, Dict[Sector, str]] = {
        ULBCategory.CLASS_I: {
            Sector.WATER_SUPPLY: "high",
            Sector.SOLID_WASTE: "high",
            Sector.URBAN_TRANSPORT: "high",
            Sector.STREETLIGHT: "medium"
        },
        ULBCategory.CLASS_II: {
            Sector.WATER_SUPPLY: "medium",
            Sector.SOLID_WASTE: "high",
            Sector.URBAN_TRANSPORT: "medium",
            Sector.STREETLIGHT: "high"
        },
        ULBCategory.CLASS_III: {
            Sector.WATER_SUPPLY: "low",
            Sector.SOLID_WASTE: "medium",
            Sector.URBAN_TRANSPORT: "low",
            Sector.STREETLIGHT: "high"
        },
        ULBCategory.NAGAR_PANCHAYAT: {
            Sector.WATER_SUPPLY: "very_low",
            Sector.SOLID_WASTE: "low",
            Sector.URBAN_TRANSPORT: "very_low",
            Sector.STREETLIGHT: "medium"
        }
    }
    
    @staticmethod
    def get_category_by_population(population: int) -> ULBCategory:
        """Determine ULB category based on population."""
        if population >= 100000:
            return ULBCategory.CLASS_I
        elif population >= 50000:
            return ULBCategory.CLASS_II
        elif population >= 20000:
            return ULBCategory.CLASS_III
        else:
            return ULBCategory.NAGAR_PANCHAYAT
    
    @staticmethod
    def get_recommended_ppp_approaches(category: ULBCategory) -> List[str]:
        """Get recommended PPP approaches for a category."""
        return ULBCategoryConfig.PPP_APPROACHES.get(category, [])
    
    @staticmethod
    def get_sector_suitability(category: ULBCategory, sector: Sector) -> str:
        """Get suitability level for a sector in a category."""
        return ULBCategoryConfig.SECTOR_SUITABILITY.get(category, {}).get(sector, "unknown")


