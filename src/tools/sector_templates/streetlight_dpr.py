"""
Streetlighting DPR Template
Easy PPP wins - lower complexity, good for smaller ULBs.
"""
from typing import Dict, Any


class StreetlightDPRTemplate:
    """
    Template for Streetlighting DPRs.
    Lower complexity, suitable for smaller ULBs and Nagar Panchayats.
    """
    
    SECTOR = "streetlight"
    FAILURE_RISK = "very_low"
    PPP_PERCENTAGE = "small_but_growing"
    
    @staticmethod
    def get_template_structure() -> Dict[str, Any]:
        """Get template structure for streetlight DPR."""
        return {
            "sections": [
                {
                    "title": "Executive Summary",
                    "required": True,
                    "key_points": [
                        "Current lighting status",
                        "Coverage gaps",
                        "Technology upgrade plan"
                    ]
                },
                {
                    "title": "Current Infrastructure",
                    "required": True,
                    "key_points": [
                        "Existing streetlights",
                        "Energy consumption",
                        "Maintenance status"
                    ]
                },
                {
                    "title": "Technical Specifications",
                    "required": True,
                    "key_points": [
                        "LED conversion",
                        "Smart lighting systems",
                        "Energy efficiency",
                        "Maintenance requirements"
                    ]
                },
                {
                    "title": "Financial Model",
                    "required": True,
                    "key_points": [
                        "Energy savings",
                        "O&M costs",
                        "Revenue sharing",
                        "Payback period"
                    ]
                },
                {
                    "title": "Implementation Plan",
                    "required": True,
                    "key_points": [
                        "Phased conversion",
                        "Technology rollout",
                        "Maintenance strategy"
                    ]
                }
            ],
            "advantages": [
                "Lower complexity",
                "Quick implementation",
                "Clear revenue model",
                "Good for smaller ULBs"
            ],
            "replication_potential": "high"
        }


