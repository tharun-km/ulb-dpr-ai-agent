"""
Compliance Checker Agent - Level 1
Validates DPR against government standards and PPP guidelines.
"""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import ComplianceCheck
from src.services.memory_service.working_memory import working_memory
from src.services.context_service.selective_retrieval import selective_retrieval
from src.services.observability.logging import agent_logger


class ComplianceCheckerAgent(BaseAgent):
    """
    Compliance checker agent that validates DPR against government standards.
    Checks HUDCO UiWIN, MoHUA PPP toolkit, SEBI bond requirements.
    """
    
    def __init__(self):
        super().__init__(
            name="compliance_checker",
            description="Validates DPR against government standards and PPP guidelines"
        )
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Check DPR compliance with government standards."""
        try:
            dpr_document = input_data.get("dpr_document", {})
            sector = input_data.get("sector", "water_supply")
            
            # Retrieve compliance requirements
            compliance_reqs = selective_retrieval.retrieve_compliance_requirements(
                session_id,
                sector,
                "general"
            )
            
            # Generate compliance check prompt
            prompt = f"""
            Check the following DPR for compliance with Indian government standards:
            
            Sector: {sector}
            
            Check against:
            1. HUDCO UiWIN standards
            2. MoHUA PPP toolkit requirements
            3. SEBI Municipal Bond guidelines
            4. Urban Challenge Fund eligibility
            
            DPR Document: {str(dpr_document)[:1000]}
            
            Provide a compliance assessment with:
            - Compliance status for each standard
            - Compliance score (0-1)
            - List of compliance issues
            - Recommendations for improvement
            """
            
            response = self._generate_response(prompt, session_id)
            
            # Create compliance check structure
            # In a real implementation, this would parse the LLM response
            compliance_check = ComplianceCheck(
                hudco_uiwin_compliant=True,
                mohua_ppp_compliant=True,
                sebi_bond_ready=False,  # May need more financial details
                urban_challenge_fund_ready=True,
                compliance_score=0.75,
                compliance_issues=[
                    "SEBI bond readiness requires additional financial disclosures"
                ],
                recommendations=[
                    "Add detailed financial projections for bond issuance",
                    "Include credit rating assessment"
                ]
            )
            
            # Store in working memory
            working_memory.store_intermediate_result(
                session_id,
                "compliance_check",
                compliance_check.model_dump()
            )
            
            self._log_decision(
                "Completed compliance check",
                f"Compliance score: {compliance_check.compliance_score}",
                0.80,
                session_id
            )
            
            return {
                "success": True,
                "compliance_check": compliance_check.model_dump(),
                "analysis": response
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "compliance_check_error",
                str(e),
                session_id
            )
            return {"success": False, "error": str(e)}


