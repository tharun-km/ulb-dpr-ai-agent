"""
Risk mitigation tools for tariff affordability, political feasibility, and public acceptance.
"""
from typing import Dict, Any, List
from src.models.dpr_schema import RiskAssessment


class TariffAffordabilityChecker:
    """Checks tariff affordability for citizens."""
    
    @staticmethod
    def check_affordability(
        proposed_tariff: float,
        average_income: float,
        current_tariff: float = 0
    ) -> Dict[str, Any]:
        """
        Check if proposed tariff is affordable.
        Generally, utilities should not exceed 5% of household income.
        """
        tariff_increase = proposed_tariff - current_tariff
        increase_percentage = (tariff_increase / current_tariff * 100) if current_tariff > 0 else 0
        income_percentage = (proposed_tariff / average_income * 100) if average_income > 0 else 0
        
        is_affordable = income_percentage <= 5.0
        is_acceptable_increase = increase_percentage <= 30.0  # Max 30% increase at once
        
        risk_level = "low"
        if not is_affordable or not is_acceptable_increase:
            risk_level = "high"
        elif income_percentage > 3.0 or increase_percentage > 20.0:
            risk_level = "medium"
        
        return {
            "is_affordable": is_affordable,
            "is_acceptable_increase": is_acceptable_increase,
            "income_percentage": income_percentage,
            "increase_percentage": increase_percentage,
            "risk_level": risk_level,
            "recommendations": TariffAffordabilityChecker._get_recommendations(
                is_affordable, is_acceptable_increase, income_percentage, increase_percentage
            )
        }
    
    @staticmethod
    def _get_recommendations(
        is_affordable: bool,
        is_acceptable_increase: bool,
        income_percentage: float,
        increase_percentage: float
    ) -> List[str]:
        """Get recommendations based on affordability analysis."""
        recommendations = []
        
        if not is_affordable:
            recommendations.append("Implement subsidy for low-income households")
            recommendations.append("Consider gradual tariff increases over 3-5 years")
        
        if not is_acceptable_increase:
            recommendations.append("Phase tariff increases in smaller increments")
            recommendations.append("Provide advance notice and public consultation")
        
        if income_percentage > 3.0:
            recommendations.append("Consider cross-subsidization from commercial users")
        
        if increase_percentage > 20.0:
            recommendations.append("Implement tariff increase in multiple phases")
            recommendations.append("Engage with citizen groups before implementation")
        
        return recommendations


class PoliticalFeasibilityAnalyzer:
    """Analyzes political feasibility of PPP projects."""
    
    @staticmethod
    def analyze_feasibility(
        state: str,
        sector: str,
        project_scale: str
    ) -> Dict[str, Any]:
        """
        Analyze political feasibility based on state, sector, and scale.
        Considers historical patterns and state-specific factors.
        """
        # Known risk factors
        high_risk_states = ["maharashtra", "karnataka"]  # Based on historical failures
        high_risk_sectors = ["water_supply"]
        
        risk_factors = []
        risk_score = 0.5  # Base score
        
        if state.lower() in high_risk_states:
            risk_factors.append(f"Historical PPP failures in {state}")
            risk_score += 0.2
        
        if sector in high_risk_sectors:
            risk_factors.append(f"High failure rate in {sector} sector")
            risk_score += 0.15
        
        if project_scale == "large":
            risk_factors.append("Large projects face more political scrutiny")
            risk_score += 0.1
        
        # Normalize risk score
        risk_score = min(1.0, risk_score)
        feasibility_score = 1.0 - risk_score
        
        return {
            "feasibility_score": feasibility_score,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "recommendations": PoliticalFeasibilityAnalyzer._get_recommendations(risk_score)
        }
    
    @staticmethod
    def _get_recommendations(risk_score: float) -> List[str]:
        """Get recommendations based on political feasibility."""
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.append("Ensure multi-party political support")
            recommendations.append("Engage with opposition parties early")
            recommendations.append("Consider state-level guarantees")
        
        if risk_score > 0.5:
            recommendations.append("Build consensus through public consultations")
            recommendations.append("Document political commitments")
        
        recommendations.append("Establish independent regulatory oversight")
        recommendations.append("Create transparent decision-making processes")
        
        return recommendations


class PublicAcceptancePredictor:
    """Predicts public acceptance based on historical patterns."""
    
    @staticmethod
    def predict_acceptance(
        sector: str,
        tariff_increase: float,
        service_improvements: List[str]
    ) -> Dict[str, Any]:
        """
        Predict public acceptance based on sector, tariff changes, and service improvements.
        """
        # Historical patterns
        high_acceptance_sectors = ["solid_waste", "streetlight"]
        low_acceptance_sectors = ["water_supply"]
        
        acceptance_score = 0.5  # Base score
        
        if sector in high_acceptance_sectors:
            acceptance_score += 0.2
        elif sector in low_acceptance_sectors:
            acceptance_score -= 0.2
        
        # Tariff impact
        if tariff_increase > 30:
            acceptance_score -= 0.3
        elif tariff_increase > 20:
            acceptance_score -= 0.15
        elif tariff_increase < 10:
            acceptance_score += 0.1
        
        # Service improvements
        if len(service_improvements) >= 3:
            acceptance_score += 0.15
        elif len(service_improvements) >= 1:
            acceptance_score += 0.1
        
        # Normalize
        acceptance_score = max(0.0, min(1.0, acceptance_score))
        
        return {
            "acceptance_score": acceptance_score,
            "predicted_resistance": 1.0 - acceptance_score,
            "recommendations": PublicAcceptancePredictor._get_recommendations(
                acceptance_score, tariff_increase
            )
        }
    
    @staticmethod
    def _get_recommendations(acceptance_score: float, tariff_increase: float) -> List[str]:
        """Get recommendations for improving public acceptance."""
        recommendations = []
        
        if acceptance_score < 0.6:
            recommendations.append("Engage with citizen groups before project launch")
            recommendations.append("Conduct public awareness campaigns")
            recommendations.append("Demonstrate clear service improvements")
        
        if tariff_increase > 20:
            recommendations.append("Justify tariff increases with service quality improvements")
            recommendations.append("Provide transparent cost breakdown")
            recommendations.append("Offer payment plans for low-income households")
        
        recommendations.append("Establish grievance redressal mechanisms")
        recommendations.append("Create citizen monitoring committees")
        
        return recommendations


class FailurePatternMatcher:
    """Matches current project against historical failure patterns."""
    
    KNOWN_FAILURES = {
        "nagpur_water": {
            "city": "Nagpur",
            "sector": "water_supply",
            "failure_reasons": [
                "Steep tariff hikes (300% increase)",
                "Public protests and political opposition",
                "Service quality issues"
            ],
            "lessons": [
                "Gradual tariff increases essential",
                "Public engagement critical",
                "Service quality must improve with tariffs"
            ]
        },
        "durg_water": {
            "city": "Durg",
            "sector": "water_supply",
            "failure_reasons": [
                "Tariff affordability concerns",
                "Political opposition",
                "Citizen-led campaigns"
            ],
            "lessons": [
                "Affordability analysis crucial",
                "Political feasibility assessment needed",
                "Early stakeholder engagement"
            ]
        }
    }
    
    @staticmethod
    def match_patterns(sector: str, proposed_tariff_increase: float) -> Dict[str, Any]:
        """Match current project against known failure patterns."""
        matches = []
        
        for failure_id, failure_data in FailurePatternMatcher.KNOWN_FAILURES.items():
            if failure_data["sector"] == sector:
                # Check tariff increase similarity
                if proposed_tariff_increase > 50:  # High risk threshold
                    matches.append({
                        "failure_case": failure_id,
                        "city": failure_data["city"],
                        "similarity": "high",
                        "risk_factors": failure_data["failure_reasons"],
                        "lessons": failure_data["lessons"]
                    })
        
        return {
            "matches": matches,
            "risk_level": "high" if len(matches) > 0 else "low",
            "recommendations": FailurePatternMatcher._get_recommendations(matches)
        }
    
    @staticmethod
    def _get_recommendations(matches: List[Dict[str, Any]]) -> List[str]:
        """Get recommendations based on failure pattern matches."""
        recommendations = []
        
        if len(matches) > 0:
            recommendations.append("Review lessons from similar failed projects")
            for match in matches:
                recommendations.extend(match.get("lessons", []))
        
        return recommendations


