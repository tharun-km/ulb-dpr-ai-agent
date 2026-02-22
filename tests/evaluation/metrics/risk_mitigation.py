"""
Risk mitigation effectiveness evaluation.
"""
from typing import Dict, Any


class RiskMitigationScorer:
    """
    Evaluates risk mitigation effectiveness in DPR.
    Checks if known failure patterns are avoided.
    """
    
    KNOWN_FAILURE_PATTERNS = {
        "high_tariff_increase": {
            "threshold": 30.0,
            "risk": "high",
            "examples": ["Nagpur", "Durg"]
        },
        "political_opposition": {
            "risk": "high",
            "examples": ["Multiple cities"]
        },
        "public_resistance": {
            "risk": "high",
            "examples": ["Nagpur", "Khandwa"]
        }
    }
    
    @staticmethod
    def evaluate_risk_mitigation(dpr_document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate risk mitigation effectiveness.
        
        Returns:
            Dictionary with risk mitigation score and analysis
        """
        risk_assessment = dpr_document.get("risk_assessment", {})
        financial_model = dpr_document.get("financial_model", {})
        
        # Check tariff affordability
        tariff_structure = financial_model.get("tariff_structure", {})
        base_tariff = tariff_structure.get("base_tariff", 0)
        
        tariff_affordability_score = risk_assessment.get("tariff_affordability_score", 0.5)
        
        # Check political feasibility
        political_feasibility_score = risk_assessment.get("political_feasibility_score", 0.5)
        
        # Check public acceptance
        public_acceptance_score = risk_assessment.get("public_acceptance_score", 0.5)
        
        # Check if failure patterns are addressed
        mitigation_recommendations = risk_assessment.get("mitigation_recommendations", [])
        failure_patterns_addressed = RiskMitigationScorer._check_failure_patterns(
            risk_assessment, mitigation_recommendations
        )
        
        # Calculate overall risk mitigation score
        risk_mitigation_score = (
            tariff_affordability_score * 0.3 +
            political_feasibility_score * 0.3 +
            public_acceptance_score * 0.2 +
            failure_patterns_addressed * 0.2
        )
        
        return {
            "risk_mitigation_score": risk_mitigation_score,
            "components": {
                "tariff_affordability": tariff_affordability_score,
                "political_feasibility": political_feasibility_score,
                "public_acceptance": public_acceptance_score,
                "failure_patterns_addressed": failure_patterns_addressed
            },
            "effective": risk_mitigation_score >= 0.7,
            "citizen_acceptability": public_acceptance_score >= 0.7,
            "recommendations": RiskMitigationScorer._get_recommendations(
                risk_mitigation_score, risk_assessment
            )
        }
    
    @staticmethod
    def _check_failure_patterns(
        risk_assessment: Dict[str, Any],
        mitigation_recommendations: List[str]
    ) -> float:
        """Check if known failure patterns are addressed."""
        score = 0.0
        
        # Check for gradual tariff increase recommendation
        if any("gradual" in rec.lower() or "phase" in rec.lower() for rec in mitigation_recommendations):
            score += 0.3
        
        # Check for public engagement
        if any("public" in rec.lower() or "citizen" in rec.lower() or "engagement" in rec.lower() 
               for rec in mitigation_recommendations):
            score += 0.3
        
        # Check for political support
        if any("political" in rec.lower() or "support" in rec.lower() 
               for rec in mitigation_recommendations):
            score += 0.2
        
        # Check overall risk score
        overall_risk = risk_assessment.get("overall_risk_score", 1.0)
        if overall_risk < 0.5:
            score += 0.2
        
        return min(1.0, score)
    
    @staticmethod
    def _get_recommendations(
        risk_mitigation_score: float,
        risk_assessment: Dict[str, Any]
    ) -> List[str]:
        """Get recommendations to improve risk mitigation."""
        recommendations = []
        
        if risk_mitigation_score < 0.7:
            recommendations.append("Strengthen tariff affordability analysis")
            recommendations.append("Enhance political feasibility assessment")
            recommendations.append("Improve public acceptance strategies")
        
        risk_factors = risk_assessment.get("risk_factors", [])
        if risk_factors:
            recommendations.append(f"Address identified risk factors: {', '.join(risk_factors[:3])}")
        
        return recommendations


