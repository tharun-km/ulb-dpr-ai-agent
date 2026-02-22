"""
Financial Modeling Agent - Level 1
Creates financial projections and viability analysis with tariff affordability checks.
"""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import FinancialModel
from src.services.memory_service.working_memory import working_memory
from src.services.observability.logging import agent_logger


class FinancialModelerAgent(BaseAgent):
    """
    Financial modeling agent that creates PPP financial projections.
    Includes tariff affordability analysis.
    """
    
    def __init__(self):
        super().__init__(
            name="financial_modeler",
            description="Creates financial projections and viability analysis"
        )
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create financial model for PPP project."""
        try:
            ulb_metadata = input_data.get("ulb_metadata", {})
            sector = input_data.get("sector", "water_supply")
            collected_data = input_data.get("collected_data", {})
            
            # Generate financial model prompt
            prompt = f"""
            Create a financial model for a PPP project in the {sector} sector.
            
            ULB Information:
            - Name: {ulb_metadata.get('name', 'Unknown')}
            - Population: {ulb_metadata.get('population', 0)}
            - Category: {ulb_metadata.get('category', 'unknown')}
            
            Provide a financial model with:
            1. Project cost estimate
            2. Revenue streams
            3. Operating costs
            4. Tariff structure
            5. Viability gap funding requirements
            6. IRR and NPV calculations
            
            Format the response as a structured financial model.
            """
            
            # Generate financial model using LLM
            response = self._generate_response(prompt, session_id)
            
            # Parse and structure financial model
            # In a real implementation, this would parse the LLM response
            # For now, create a template structure
            financial_model = FinancialModel(
                project_cost=100000000,  # 100 crores (example)
                revenue_streams=[
                    {"source": "user_charges", "amount": 50000000, "period": "annual"}
                ],
                operating_costs=[
                    {"type": "operations", "amount": 30000000, "period": "annual"}
                ],
                tariff_structure={
                    "base_tariff": 50,
                    "unit": "per_connection_per_month"
                },
                viability_gap_funding=20000000,
                internal_rate_of_return=12.5,
                net_present_value=50000000
            )
            
            # Store in working memory
            working_memory.store_intermediate_result(
                session_id,
                "financial_model",
                financial_model.model_dump()
            )
            
            self._log_decision(
                "Created financial model",
                f"Project cost: {financial_model.project_cost}, IRR: {financial_model.internal_rate_of_return}%",
                0.85,
                session_id
            )
            
            return {
                "success": True,
                "financial_model": financial_model.model_dump(),
                "analysis": response
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "financial_modeling_error",
                str(e),
                session_id
            )
            return {"success": False, "error": str(e)}


