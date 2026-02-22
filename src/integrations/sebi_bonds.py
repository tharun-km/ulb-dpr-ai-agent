"""
SEBI Municipal Bond guidelines integration for financing readiness.
"""
from typing import Dict, Any, Optional
from src.utils.config import config


class SEBIBondsIntegration:
    """
    Integration with SEBI Municipal Bond guidelines.
    Assesses bond issuance readiness and requirements.
    """
    
    def __init__(self):
        self.api_key = config.sebi_api_key
        self.base_url = "https://sebi.gov.in"  # Example URL
    
    def get_bond_requirements(self) -> Dict[str, Any]:
        """
        Get SEBI Municipal Bond issuance requirements.
        """
        return {
            "eligibility_criteria": [
                "Credit rating of at least BBB",
                "Audited accounts for last 3 years",
                "Transparent disclosures",
                "Bankable project pipeline"
            ],
            "documentation_required": [
                "Credit rating report",
                "Audited financial statements",
                "Project DPR",
                "Revenue projections",
                "Risk assessment"
            ],
            "minimum_project_size": 100000000,  # 100 crores
            "credit_rating_requirements": {
                "minimum": "BBB",
                "preferred": "A or above"
            }
    }
    
    def assess_bond_readiness(self, ulb_data: Dict[str, Any], dpr_document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess ULB readiness for municipal bond issuance.
        """
        requirements = self.get_bond_requirements()
        
        readiness_assessment = {
            "ready": False,
            "score": 0.0,
            "requirements_met": [],
            "requirements_missing": [],
            "recommendations": []
        }
        
        # Check credit rating
        credit_rating = ulb_data.get("credit_rating", "not_rated")
        if credit_rating and credit_rating >= "BBB":
            readiness_assessment["requirements_met"].append("credit_rating")
        else:
            readiness_assessment["requirements_missing"].append("credit_rating")
            readiness_assessment["recommendations"].append("Obtain credit rating of BBB or above")
        
        # Check audited accounts
        has_audited_accounts = ulb_data.get("has_audited_accounts", False)
        if has_audited_accounts:
            readiness_assessment["requirements_met"].append("audited_accounts")
        else:
            readiness_assessment["requirements_missing"].append("audited_accounts")
            readiness_assessment["recommendations"].append("Maintain audited accounts for 3 years")
        
        # Check project size
        project_cost = dpr_document.get("financial_model", {}).get("project_cost", 0)
        if project_cost >= requirements["minimum_project_size"]:
            readiness_assessment["requirements_met"].append("project_size")
        else:
            readiness_assessment["requirements_missing"].append("project_size")
            readiness_assessment["recommendations"].append(
                f"Project size should be at least {requirements['minimum_project_size']}"
            )
        
        # Calculate readiness score
        total_requirements = len(requirements["eligibility_criteria"])
        met_requirements = len(readiness_assessment["requirements_met"])
        readiness_assessment["score"] = met_requirements / total_requirements if total_requirements > 0 else 0.0
        readiness_assessment["ready"] = readiness_assessment["score"] >= 0.75
        
        return readiness_assessment
    
    def get_financing_alternatives(self, bond_readiness: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get alternative financing options if bond issuance not ready.
        """
        if bond_readiness["ready"]:
            return {
                "primary_option": "municipal_bonds",
                "alternatives": []
            }
        
        return {
            "primary_option": "viability_gap_funding",
            "alternatives": [
                "State government grants",
                "Central government schemes",
                "Multilateral funding",
                "Pooled financing with other ULBs"
            ],
            "recommendations": bond_readiness.get("recommendations", [])
        }


