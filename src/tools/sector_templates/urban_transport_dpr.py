"""
Urban Transport DPR Template
38% of urban PPPs, mostly BRTS - focus on public transport systems.
"""
from typing import Dict, Any


class UrbanTransportDPRTemplate:
    """
    Template for Urban Transport DPRs.
    Focus on BRTS and public transport systems.
    """
    
    SECTOR = "urban_transport"
    FAILURE_RISK = "medium"
    PPP_PERCENTAGE = 38
    
    @staticmethod
    def get_template_structure() -> Dict[str, Any]:
        """Get template structure for urban transport DPR."""
        return {
            "sections": [
                {
                    "title": "Executive Summary",
                    "required": True,
                    "key_points": [
                        "Transport demand assessment",
                        "System design",
                        "Investment requirements"
                    ]
                },
                {
                    "title": "Current Transport Infrastructure",
                    "required": True,
                    "key_points": [
                        "Existing routes",
                        "Fleet composition",
                        "Ridership patterns",
                        "Gap analysis"
                    ]
                },
                {
                    "title": "BRTS/Public Transport Design",
                    "required": True,
                    "key_points": [
                        "Route planning",
                        "Fleet requirements",
                        "Infrastructure needs",
                        "Technology integration"
                    ]
                },
                {
                    "title": "Financial Model",
                    "required": True,
                    "key_points": [
                        "Fare structure",
                        "Revenue projections",
                        "Subsidy requirements",
                        "O&M costs"
                    ]
                },
                {
                    "title": "Integration with PM Gati Shakti",
                    "required": True,
                    "key_points": [
                        "Multi-modal connectivity",
                        "Infrastructure alignment",
                        "National transport network"
                    ]
                },
                {
                    "title": "Implementation Plan",
                    "required": True,
                    "key_points": [
                        "Phased implementation",
                        "Stakeholder coordination",
                        "Timeline"
                    ]
                }
            ],
            "key_considerations": [
                "Integration with existing transport",
                "Affordability of fares",
                "Last-mile connectivity",
                "Environmental impact"
            ]
        }


