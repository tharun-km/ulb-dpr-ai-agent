"""
Solid Waste Management DPR Template
37% of urban PPPs, more successful - good template for replication.
"""
from typing import Dict, Any


class SolidWasteDPRTemplate:
    """
    Template for Solid Waste Management DPRs.
    Based on successful PPP models.
    """
    
    SECTOR = "solid_waste"
    FAILURE_RISK = "low"
    PPP_PERCENTAGE = 37
    
    @staticmethod
    def get_template_structure() -> Dict[str, Any]:
        """Get template structure for solid waste DPR."""
        return {
            "sections": [
                {
                    "title": "Executive Summary",
                    "required": True,
                    "key_points": [
                        "Waste generation assessment",
                        "Collection and transportation plan",
                        "Processing and disposal strategy"
                    ]
                },
                {
                    "title": "Current Waste Management Status",
                    "required": True,
                    "key_points": [
                        "Waste generation rates",
                        "Collection coverage",
                        "Processing facilities",
                        "Disposal sites"
                    ]
                },
                {
                    "title": "Technical Specifications",
                    "required": True,
                    "key_points": [
                        "Collection system design",
                        "Transportation fleet",
                        "Processing technology",
                        "Landfill requirements"
                    ]
                },
                {
                    "title": "Financial Model",
                    "required": True,
                    "key_points": [
                        "Collection charges",
                        "Processing fees",
                        "Revenue from recyclables",
                        "O&M costs"
                    ]
                },
                {
                    "title": "Environmental Compliance",
                    "required": True,
                    "key_points": [
                        "SWM Rules 2016 compliance",
                        "Environmental clearances",
                        "Pollution control measures"
                    ]
                },
                {
                    "title": "Implementation Plan",
                    "required": True,
                    "key_points": [
                        "Phased rollout",
                        "Community engagement",
                        "Monitoring mechanisms"
                    ]
                }
            ],
            "success_factors": [
                "Clear service level agreements",
                "Adequate revenue streams",
                "Community participation",
                "Technology selection"
            ],
            "replication_guidelines": [
                "Adapt from Raipur/Bilaspur models",
                "Scale to ULB size",
                "Local context adaptation"
            ]
        }


