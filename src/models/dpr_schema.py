"""
Data models for DPR (Detailed Project Report) structure.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class Sector(str, Enum):
    """Infrastructure sectors for DPR creation."""
    WATER_SUPPLY = "water_supply"
    SOLID_WASTE = "solid_waste"
    URBAN_TRANSPORT = "urban_transport"
    STREETLIGHT = "streetlight"


class ULBCategory(str, Enum):
    """ULB size categories."""
    CLASS_I = "class_i"  # 100k+ population
    CLASS_II = "class_ii"  # 50k-100k
    CLASS_III = "class_iii"  # 20k-50k
    NAGAR_PANCHAYAT = "nagar_panchayat"  # <20k


class DPRStatus(str, Enum):
    """DPR creation status."""
    INITIALIZED = "initialized"
    DATA_COLLECTION = "data_collection"
    FINANCIAL_MODELING = "financial_modeling"
    DOCUMENT_GENERATION = "document_generation"
    COMPLIANCE_CHECK = "compliance_check"
    RISK_ASSESSMENT = "risk_assessment"
    COMPLETED = "completed"
    FAILED = "failed"


class ULBMetadata(BaseModel):
    """Metadata about a ULB."""
    name: str
    state: str
    category: ULBCategory
    population: int
    existing_infrastructure: Dict[str, Any] = Field(default_factory=dict)
    financial_status: Dict[str, Any] = Field(default_factory=dict)


class FinancialModel(BaseModel):
    """Financial model for PPP project."""
    project_cost: float
    revenue_streams: List[Dict[str, Any]]
    operating_costs: List[Dict[str, Any]]
    tariff_structure: Dict[str, Any]
    viability_gap_funding: Optional[float] = None
    internal_rate_of_return: Optional[float] = None
    net_present_value: Optional[float] = None


class RiskAssessment(BaseModel):
    """Risk assessment results."""
    tariff_affordability_score: float = Field(ge=0, le=1)
    political_feasibility_score: float = Field(ge=0, le=1)
    public_acceptance_score: float = Field(ge=0, le=1)
    historical_failure_risk: float = Field(ge=0, le=1)
    overall_risk_score: float = Field(ge=0, le=1)
    risk_factors: List[str] = Field(default_factory=list)
    mitigation_recommendations: List[str] = Field(default_factory=list)


class ComplianceCheck(BaseModel):
    """Compliance check results."""
    hudco_uiwin_compliant: bool = False
    mohua_ppp_compliant: bool = False
    sebi_bond_ready: bool = False
    urban_challenge_fund_ready: bool = False
    compliance_score: float = Field(ge=0, le=1)
    compliance_issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class DPRDocument(BaseModel):
    """Complete DPR document structure."""
    ulb_metadata: ULBMetadata
    sector: Sector
    project_title: str
    executive_summary: str
    project_description: str
    technical_specifications: Dict[str, Any]
    financial_model: FinancialModel
    risk_assessment: RiskAssessment
    compliance_check: ComplianceCheck
    implementation_plan: Dict[str, Any]
    status: DPRStatus = DPRStatus.INITIALIZED
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


