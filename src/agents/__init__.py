"""
Multi-agent system for DPR creation.
"""
from .base_agent import BaseAgent
from .orchestrator import OrchestratorAgent
from .data_collector import DataCollectorAgent
from .financial_modeler import FinancialModelerAgent
from .document_generator import DocumentGeneratorAgent
from .compliance_checker import ComplianceCheckerAgent
from .risk_assessment_agent import RiskAssessmentAgent

__all__ = [
    "BaseAgent",
    "OrchestratorAgent",
    "DataCollectorAgent",
    "FinancialModelerAgent",
    "DocumentGeneratorAgent",
    "ComplianceCheckerAgent",
    "RiskAssessmentAgent"
]


