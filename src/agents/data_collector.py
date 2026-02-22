"""
Data Collection Agent - Level 1
Gathers ULB-specific data (population, existing infrastructure, financial status).
"""
import asyncio
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import ULBMetadata, ULBCategory
from src.models.ulb_categories import ULBCategoryConfig
from src.services.memory_service.working_memory import working_memory
from src.services.observability.logging import agent_logger


class DataCollectorAgent(BaseAgent):
    """
    Data collection agent that gathers ULB-specific information.
    Can work in parallel with other data collection tasks.
    """
    
    def __init__(self):
        super().__init__(
            name="data_collector",
            description="Gathers ULB-specific data for DPR creation"
        )
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Collect ULB data for DPR creation."""
        try:
            ulb_metadata_input = input_data.get("ulb_metadata", {})
            sector = input_data.get("sector", "water_supply")
            
            # Extract ULB information
            ulb_name = ulb_metadata_input.get("name", "Unknown ULB")
            state = ulb_metadata_input.get("state", "chhattisgarh")
            population = ulb_metadata_input.get("population", 0)
            
            # Determine ULB category
            category = ULBCategoryConfig.get_category_by_population(population)
            
            # Create ULB metadata
            ulb_metadata = ULBMetadata(
                name=ulb_name,
                state=state,
                category=category,
                population=population,
                existing_infrastructure=ulb_metadata_input.get("existing_infrastructure", {}),
                financial_status=ulb_metadata_input.get("financial_status", {})
            )
            
            # Store in working memory
            working_memory.store_data(session_id, "ulb_metadata", ulb_metadata.model_dump())
            working_memory.store_data(session_id, "sector", sector)
            working_memory.store_data(session_id, "ulb_category", category.value)
            
            # Log decision
            self._log_decision(
                f"Collected data for {ulb_name}",
                f"ULB category: {category.value}, Population: {population}",
                0.95,
                session_id
            )
            
            # Collect additional data (in a real implementation, this would query databases/APIs)
            collected_data = {
                "population": population,
                "category": category.value,
                "sector": sector,
                "state": state,
                "existing_infrastructure": ulb_metadata.existing_infrastructure,
                "financial_status": ulb_metadata.financial_status
            }
            
            working_memory.store_data(session_id, "collected_data", collected_data)
            
            return {
                "success": True,
                "ulb_metadata": ulb_metadata.model_dump(),
                "data": collected_data,
                "category": category.value
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "data_collection_error",
                str(e),
                session_id
            )
            return {"success": False, "error": str(e)}


