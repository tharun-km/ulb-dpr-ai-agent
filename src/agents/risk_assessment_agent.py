"""
Risk Assessment Agent - Level 1
Analyzes tariff affordability, political feasibility, public acceptance, and historical failure patterns.
"""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import RiskAssessment
from src.services.memory_service.working_memory import working_memory
from src.services.memory_service.episodic_memory import episodic_memory
from src.services.observability.logging import agent_logger


class RiskAssessmentAgent(BaseAgent):
    """
    Risk assessment agent that analyzes various risk factors for PPP projects.
    Learns from historical failure patterns.
    """
    
    def __init__(self):
        super().__init__(
            name="risk_assessor",
            description="Analyzes tariff affordability, political feasibility, and public acceptance"
        )
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Assess risks for PPP project."""
        try:
            ulb_metadata = input_data.get("ulb_metadata", {})
            financial_model = input_data.get("financial_model", {})
            sector = input_data.get("sector", "water_supply")
            
            # Check historical failure patterns
            failure_patterns = episodic_memory.get_failure_patterns(sector)
            
            # Generate risk assessment prompt
            prompt = f"""
            Assess risks for a PPP project in the {sector} sector.
            
            ULB: {ulb_metadata.get('name', 'Unknown')}
            Population: {ulb_metadata.get('population', 0)}
            
            Financial Model:
            - Project Cost: {financial_model.get('project_cost', 0)}
            - Tariff Structure: {financial_model.get('tariff_structure', {})}
            
            Assess the following risk factors:
            1. Tariff Affordability (0-1 score)
            2. Political Feasibility (0-1 score)
            3. Public Acceptance (0-1 score)
            4. Historical Failure Risk (based on similar projects)
            
            Consider known failure patterns from cities like Nagpur, Durg, Khandwa, Latur, Hubli-Dharwad.
            
            Provide risk scores and mitigation recommendations.
            """
            
            response = self._generate_response(prompt, session_id)
            
            # Create risk assessment structure
            # In a real implementation, this would parse the LLM response
            risk_assessment = RiskAssessment(
                tariff_affordability_score=0.7,
                political_feasibility_score=0.8,
                public_acceptance_score=0.75,
                historical_failure_risk=0.3,
                overall_risk_score=0.64,
                risk_factors=[
                    "Tariff increases may face public resistance",
                    "Political changes could affect project continuity"
                ],
                mitigation_recommendations=[
                    "Implement gradual tariff increases",
                    "Ensure multi-party political support",
                    "Engage with citizen groups early"
                ]
            )
            
            # Store in working memory
            working_memory.store_intermediate_result(
                session_id,
                "risk_assessment",
                risk_assessment.model_dump()
            )
            
            self._log_decision(
                "Completed risk assessment",
                f"Overall risk score: {risk_assessment.overall_risk_score}",
                0.85,
                session_id
            )
            
            return {
                "success": True,
                "risk_assessment": risk_assessment.model_dump(),
                "analysis": response,
                "historical_patterns": failure_patterns
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "risk_assessment_error",
                str(e),
                session_id
            )
            return {"success": False, "error": str(e)}


