"""
Bankability scoring metrics for DPR evaluation.
"""
from typing import Dict, Any
from src.models.dpr_schema import DPRDocument, ComplianceCheck


class BankabilityScorer:
    """
    Scores DPR bankability based on HUDCO/UiWIN standards,
    Urban Challenge Fund readiness, and credit-rating readiness.
    """
    
    @staticmethod
    def calculate_bankability_score(dpr_document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall bankability score.
        
        Returns:
            Dictionary with bankability score and breakdown
        """
        score_components = {
            "hudco_compliance": 0.0,
            "mohua_compliance": 0.0,
            "financial_viability": 0.0,
            "technical_feasibility": 0.0,
            "credit_rating_ready": 0.0
        }
        
        # Check HUDCO compliance
        compliance_check = dpr_document.get("compliance_check", {})
        if compliance_check.get("hudco_uiwin_compliant", False):
            score_components["hudco_compliance"] = 1.0
        else:
            score_components["hudco_compliance"] = compliance_check.get("compliance_score", 0.0)
        
        # Check MoHUA compliance
        if compliance_check.get("mohua_ppp_compliant", False):
            score_components["mohua_compliance"] = 1.0
        else:
            score_components["mohua_compliance"] = compliance_check.get("compliance_score", 0.0)
        
        # Check financial viability
        financial_model = dpr_document.get("financial_model", {})
        irr = financial_model.get("internal_rate_of_return", 0)
        npv = financial_model.get("net_present_value", 0)
        
        if irr >= 12.0 and npv > 0:
            score_components["financial_viability"] = 1.0
        elif irr >= 10.0 and npv > 0:
            score_components["financial_viability"] = 0.75
        else:
            score_components["financial_viability"] = 0.5
        
        # Technical feasibility (simplified check)
        technical_specs = dpr_document.get("technical_specifications", {})
        if technical_specs:
            score_components["technical_feasibility"] = 0.8
        else:
            score_components["technical_feasibility"] = 0.3
        
        # Credit rating readiness
        if compliance_check.get("sebi_bond_ready", False):
            score_components["credit_rating_ready"] = 1.0
        else:
            score_components["credit_rating_ready"] = 0.5
        
        # Calculate weighted average
        weights = {
            "hudco_compliance": 0.25,
            "mohua_compliance": 0.25,
            "financial_viability": 0.30,
            "technical_feasibility": 0.10,
            "credit_rating_ready": 0.10
        }
        
        overall_score = sum(
            score_components[key] * weights[key]
            for key in score_components
        )
        
        return {
            "overall_score": overall_score,
            "components": score_components,
            "bankable": overall_score >= 0.75,
            "urban_challenge_fund_ready": compliance_check.get("urban_challenge_fund_ready", False),
            "recommendations": BankabilityScorer._get_recommendations(score_components)
        }
    
    @staticmethod
    def _get_recommendations(components: Dict[str, float]) -> list:
        """Get recommendations to improve bankability."""
        recommendations = []
        
        if components["hudco_compliance"] < 0.75:
            recommendations.append("Improve HUDCO UiWIN compliance")
        
        if components["mohua_compliance"] < 0.75:
            recommendations.append("Enhance MoHUA PPP toolkit compliance")
        
        if components["financial_viability"] < 0.75:
            recommendations.append("Strengthen financial model - target IRR >= 12%")
        
        if components["credit_rating_ready"] < 0.75:
            recommendations.append("Prepare for credit rating - ensure audited accounts")
        
        return recommendations


