"""
Water Supply & Sewerage DPR Template
25% of urban PPPs but high failure rate - requires careful risk mitigation.
"""
from typing import Dict, Any


class WaterSupplyDPRTemplate:
    """
    Template for Water Supply & Sewerage DPRs.
    Includes specific sections for water infrastructure projects.
    """
    
    SECTOR = "water_supply"
    FAILURE_RISK = "high"
    PPP_PERCENTAGE = 25
    
    @staticmethod
    def get_template_structure() -> Dict[str, Any]:
        """Get template structure for water supply DPR."""
        return {
            "sections": [
                {
                    "title": "Executive Summary",
                    "required": True,
                    "key_points": [
                        "Project scope and objectives",
                        "Investment requirements",
                        "Expected outcomes"
                    ]
                },
                {
                    "title": "Current Water Supply Status",
                    "required": True,
                    "key_points": [
                        "Existing infrastructure",
                        "Coverage and service levels",
                        "Water quality parameters",
                        "Operational efficiency"
                    ]
                },
                {
                    "title": "Project Scope and Technical Specifications",
                    "required": True,
                    "key_points": [
                        "Water treatment capacity",
                        "Distribution network design",
                        "Sewerage system specifications",
                        "Technology selection"
                    ]
                },
                {
                    "title": "Financial Model",
                    "required": True,
                    "key_points": [
                        "Capital investment",
                        "Tariff structure",
                        "Revenue projections",
                        "O&M costs",
                        "VGF requirements"
                    ]
                },
                {
                    "title": "Risk Mitigation",
                    "required": True,
                    "key_points": [
                        "Tariff affordability analysis",
                        "Political feasibility",
                        "Public acceptance strategy",
                        "Lessons from Nagpur, Durg failures"
                    ]
                },
                {
                    "title": "Implementation Plan",
                    "required": True,
                    "key_points": [
                        "Phased implementation",
                        "Procurement strategy",
                        "Timeline and milestones"
                    ]
                }
            ],
            "risk_factors": [
                "Steep tariff hikes leading to public resistance",
                "Political opposition to privatization",
                "Water quality concerns",
                "Service delivery failures"
            ],
            "mitigation_strategies": [
                "Gradual tariff increases",
                "Transparent public engagement",
                "Performance guarantees",
                "Regulatory oversight"
            ]
        }
    
    @staticmethod
    def get_financial_model_guidelines() -> Dict[str, Any]:
        """Get financial modeling guidelines for water supply."""
        return {
            "revenue_streams": [
                "Water supply charges",
                "Sewerage charges",
                "Connection charges",
                "Penalty charges"
            ],
            "cost_components": [
                "Water treatment costs",
                "Distribution O&M",
                "Sewerage treatment",
                "Administrative costs"
            ],
            "tariff_considerations": [
                "Affordability for low-income households",
                "Cost recovery",
                "Inflation indexing",
                "Subsidy mechanisms"
            ]
        }


