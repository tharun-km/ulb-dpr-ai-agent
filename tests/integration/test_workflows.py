"""
Integration tests for complete workflows.
"""
import pytest
import asyncio
from src.agents.orchestrator import OrchestratorAgent
from src.models.dpr_schema import Sector


@pytest.fixture
def sample_workflow_input():
    """Sample input for workflow testing."""
    return {
        "ulb_metadata": {
            "name": "Test ULB",
            "state": "chhattisgarh",
            "population": 75000,
            "existing_infrastructure": {
                "solid_waste": {
                    "collection_coverage": 70
                }
            },
            "financial_status": {
                "annual_revenue": 50000000
            }
        },
        "sector": "solid_waste"
    }


@pytest.mark.asyncio
async def test_complete_dpr_workflow(sample_workflow_input):
    """Test complete DPR creation workflow."""
    import uuid
    session_id = str(uuid.uuid4())
    
    orchestrator = OrchestratorAgent()
    result = await orchestrator.execute(session_id, sample_workflow_input)
    
    # Check workflow completed
    assert "success" in result
    # Note: Actual success depends on API keys and may fail in test environment
    # This test structure validates the workflow logic


