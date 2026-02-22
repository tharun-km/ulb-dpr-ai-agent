"""
Unit tests for agents.
"""
import pytest
import asyncio
from src.agents.data_collector import DataCollectorAgent
from src.agents.financial_modeler import FinancialModelerAgent
from src.models.dpr_schema import Sector, ULBCategory


@pytest.fixture
def sample_session_id():
    """Sample session ID for testing."""
    return "test_session_123"


@pytest.fixture
def sample_ulb_data():
    """Sample ULB data for testing."""
    return {
        "ulb_metadata": {
            "name": "Test ULB",
            "state": "chhattisgarh",
            "population": 75000,
            "existing_infrastructure": {},
            "financial_status": {}
        },
        "sector": "solid_waste"
    }


@pytest.mark.asyncio
async def test_data_collector_agent(sample_session_id, sample_ulb_data):
    """Test data collection agent."""
    agent = DataCollectorAgent()
    result = await agent.execute(sample_session_id, sample_ulb_data)
    
    assert result["success"] is True
    assert "ulb_metadata" in result
    assert "data" in result
    assert result["ulb_metadata"]["name"] == "Test ULB"


@pytest.mark.asyncio
async def test_financial_modeler_agent(sample_session_id):
    """Test financial modeling agent."""
    agent = FinancialModelerAgent()
    input_data = {
        "ulb_metadata": {
            "name": "Test ULB",
            "population": 75000
        },
        "sector": "solid_waste",
        "collected_data": {}
    }
    
    result = await agent.execute(sample_session_id, input_data)
    
    assert result["success"] is True
    assert "financial_model" in result
    assert "project_cost" in result["financial_model"]


def test_ulb_category_determination():
    """Test ULB category determination."""
    from src.models.ulb_categories import ULBCategoryConfig
    
    assert ULBCategoryConfig.get_category_by_population(150000) == ULBCategory.CLASS_I
    assert ULBCategoryConfig.get_category_by_population(75000) == ULBCategory.CLASS_II
    assert ULBCategoryConfig.get_category_by_population(30000) == ULBCategory.CLASS_III
    assert ULBCategoryConfig.get_category_by_population(15000) == ULBCategory.NAGAR_PANCHAYAT


