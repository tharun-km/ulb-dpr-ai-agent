"""
Main entry point for ULB DPR Assistant Agent.
"""
import asyncio
import sys
from typing import Dict, Any
from src.agents.orchestrator import OrchestratorAgent
from src.models.dpr_schema import Sector, ULBMetadata
from src.services.session_service import session_service
from src.services.observability.logging import agent_logger
from src.services.observability.metrics import metrics_collector


async def create_dpr(
    ulb_name: str,
    state: str,
    population: int,
    sector: str,
    session_id: str = None
) -> Dict[str, Any]:
    """
    Create a DPR for a ULB.
    
    Args:
        ulb_name: Name of the ULB
        state: State name
        population: ULB population
        sector: Infrastructure sector (water_supply, solid_waste, urban_transport, streetlight)
        session_id: Optional session ID
    
    Returns:
        Dictionary with DPR creation results
    """
    if not session_id:
        import uuid
        session_id = str(uuid.uuid4())
    
    # Create orchestrator agent
    orchestrator = OrchestratorAgent()
    
    # Prepare input data
    ulb_metadata = ULBMetadata(
        name=ulb_name,
        state=state,
        category=None,  # Will be determined by population
        population=population,
        existing_infrastructure={},
        financial_status={}
    )
    
    input_data = {
        "ulb_metadata": ulb_metadata.model_dump(),
        "sector": sector
    }
    
    # Execute orchestrator
    result = await orchestrator.execute(session_id, input_data)
    
    # Record metrics
    if result.get("success"):
        metrics_collector.record_dpr_created(sector, ulb_metadata.category.value if ulb_metadata.category else "unknown")
    
    return result


async def main():
    """Main function for CLI usage."""
    if len(sys.argv) < 5:
        print("Usage: python src/main.py <ulb_name> <state> <population> <sector>")
        print("Example: python src/main.py 'Raipur' 'chhattisgarh' 1010000 'solid_waste'")
        sys.exit(1)
    
    ulb_name = sys.argv[1]
    state = sys.argv[2]
    population = int(sys.argv[3])
    sector = sys.argv[4]
    
    print(f"Creating DPR for {ulb_name}, {state}")
    print(f"Population: {population}, Sector: {sector}")
    print("-" * 50)
    
    result = await create_dpr(ulb_name, state, population, sector)
    
    if result.get("success"):
        print("\n✓ DPR created successfully!")
        print(f"Status: {result.get('dpr_document', {}).get('status', 'unknown')}")
        print(f"Project Title: {result.get('dpr_document', {}).get('project_title', 'N/A')}")
    else:
        print(f"\n✗ DPR creation failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(main())


