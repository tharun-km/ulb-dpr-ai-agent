"""
Unit tests for tools.
"""
import pytest
from src.tools.risk_mitigation import (
    TariffAffordabilityChecker,
    PoliticalFeasibilityAnalyzer,
    PublicAcceptancePredictor,
    FailurePatternMatcher
)
from src.tools.aggregation_intelligence import AggregationIntelligence
from src.models.dpr_schema import Sector, ULBCategory


def test_tariff_affordability_checker():
    """Test tariff affordability checking."""
    result = TariffAffordabilityChecker.check_affordability(
        proposed_tariff=500,
        average_income=10000,
        current_tariff=300
    )
    
    assert "is_affordable" in result
    assert "risk_level" in result
    assert "recommendations" in result


def test_political_feasibility_analyzer():
    """Test political feasibility analysis."""
    result = PoliticalFeasibilityAnalyzer.analyze_feasibility(
        state="chhattisgarh",
        sector="water_supply",
        project_scale="medium"
    )
    
    assert "feasibility_score" in result
    assert "risk_factors" in result
    assert "recommendations" in result


def test_public_acceptance_predictor():
    """Test public acceptance prediction."""
    result = PublicAcceptancePredictor.predict_acceptance(
        sector="solid_waste",
        tariff_increase=15.0,
        service_improvements=["Better collection", "Processing facility"]
    )
    
    assert "acceptance_score" in result
    assert "recommendations" in result


def test_failure_pattern_matcher():
    """Test failure pattern matching."""
    result = FailurePatternMatcher.match_patterns(
        sector="water_supply",
        proposed_tariff_increase=60.0
    )
    
    assert "matches" in result
    assert "risk_level" in result


def test_aggregation_intelligence():
    """Test aggregation intelligence."""
    ulbs = [
        {"name": "ULB1", "category": "class_ii", "population": 60000},
        {"name": "ULB2", "category": "class_ii", "population": 55000},
        {"name": "ULB3", "category": "class_ii", "population": 65000}
    ]
    
    result = AggregationIntelligence.identify_clustering_opportunities(
        ulbs=ulbs,
        sector=Sector.SOLID_WASTE,
        min_cluster_size=3
    )
    
    assert "clusters" in result
    assert "recommendations" in result


