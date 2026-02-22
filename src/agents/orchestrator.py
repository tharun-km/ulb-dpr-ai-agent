"""
Orchestrator Agent - Level 2-3
Main coordinator that manages the DPR creation workflow with strategic planning.
"""
import asyncio
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import DPRStatus, DPRDocument, Sector, ULBMetadata
from src.services.session_service import session_service
from src.services.memory_service.working_memory import working_memory
from src.services.observability.logging import agent_logger


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator agent that coordinates the multi-agent DPR creation workflow.
    Implements Level 2-3 maturity with strategic planning and coordination.
    """
    
    def __init__(self):
        super().__init__(
            name="orchestrator",
            description="Main coordinator managing DPR creation workflow"
        )
        # Initialize sub-agents (lazy import to avoid circular dependencies)
        from src.agents.data_collector import DataCollectorAgent
        from src.agents.financial_modeler import FinancialModelerAgent
        from src.agents.document_generator import DocumentGeneratorAgent
        from src.agents.compliance_checker import ComplianceCheckerAgent
        from src.agents.risk_assessment_agent import RiskAssessmentAgent
        
        self.data_collector = DataCollectorAgent()
        self.financial_modeler = FinancialModelerAgent()
        self.document_generator = DocumentGeneratorAgent()
        self.compliance_checker = ComplianceCheckerAgent()
        self.risk_assessor = RiskAssessmentAgent()
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate the complete DPR creation workflow.
        
        Workflow:
        1. Data Collection (parallel where possible)
        2. Financial Modeling
        3. Risk Assessment
        4. Document Generation
        5. Compliance Check
        6. Final Review
        """
        try:
            # Initialize session
            if not session_service.get_session(session_id):
                session_service.create_session(session_id, input_data)
            
            working_memory.initialize_context(session_id)
            session_service.update_status(session_id, DPRStatus.DATA_COLLECTION)
            
            agent_logger.log_status_change(
                session_id,
                "initialized",
                DPRStatus.DATA_COLLECTION.value,
                "Starting DPR creation workflow"
            )
            
            # Step 1: Data Collection
            agent_logger.log_agent_decision(
                self.name,
                "workflow_step",
                "Starting data collection phase",
                0.9,
                session_id
            )
            
            ulb_metadata = input_data.get("ulb_metadata", {})
            sector = Sector(input_data.get("sector", "water_supply"))
            
            data_result = await self.data_collector.execute(
                session_id,
                {
                    "ulb_metadata": ulb_metadata,
                    "sector": sector.value
                }
            )
            
            if not data_result.get("success"):
                session_service.update_status(session_id, DPRStatus.FAILED)
                return {"success": False, "error": "Data collection failed"}
            
            # Step 2: Financial Modeling
            session_service.update_status(session_id, DPRStatus.FINANCIAL_MODELING)
            working_memory.update_current_step(session_id, "financial_modeling")
            
            financial_result = await self.financial_modeler.execute(
                session_id,
                {
                    "ulb_metadata": data_result.get("ulb_metadata"),
                    "sector": sector.value,
                    "collected_data": data_result.get("data", {})
                },
                data_result
            )
            
            if not financial_result.get("success"):
                session_service.update_status(session_id, DPRStatus.FAILED)
                return {"success": False, "error": "Financial modeling failed"}
            
            # Step 3: Risk Assessment
            session_service.update_status(session_id, DPRStatus.RISK_ASSESSMENT)
            working_memory.update_current_step(session_id, "risk_assessment")
            
            risk_result = await self.risk_assessor.execute(
                session_id,
                {
                    "ulb_metadata": data_result.get("ulb_metadata"),
                    "financial_model": financial_result.get("financial_model", {}),
                    "sector": sector.value
                },
                {**data_result, **financial_result}
            )
            
            # Step 4: Document Generation
            session_service.update_status(session_id, DPRStatus.DOCUMENT_GENERATION)
            working_memory.update_current_step(session_id, "document_generation")
            
            document_result = await self.document_generator.execute(
                session_id,
                {
                    "ulb_metadata": data_result.get("ulb_metadata"),
                    "financial_model": financial_result.get("financial_model", {}),
                    "risk_assessment": risk_result.get("risk_assessment", {}),
                    "sector": sector.value,
                    "collected_data": data_result.get("data", {})
                },
                {**data_result, **financial_result, **risk_result}
            )
            
            if not document_result.get("success"):
                session_service.update_status(session_id, DPRStatus.FAILED)
                return {"success": False, "error": "Document generation failed"}
            
            # Step 5: Compliance Check
            session_service.update_status(session_id, DPRStatus.COMPLIANCE_CHECK)
            working_memory.update_current_step(session_id, "compliance_check")
            
            compliance_result = await self.compliance_checker.execute(
                session_id,
                {
                    "dpr_document": document_result.get("dpr_document", {}),
                    "sector": sector.value
                },
                document_result
            )
            
            # Step 6: Finalize DPR
            dpr_document = document_result.get("dpr_document")
            if dpr_document:
                dpr_document["compliance_check"] = compliance_result.get("compliance_check", {})
                dpr_document["status"] = DPRStatus.COMPLETED.value
                
                # Store in session
                from src.models.dpr_schema import DPRDocument
                dpr = DPRDocument(**dpr_document)
                session_service.store_dpr_document(session_id, dpr)
            
            session_service.update_status(session_id, DPRStatus.COMPLETED)
            agent_logger.log_status_change(
                session_id,
                DPRStatus.COMPLIANCE_CHECK.value,
                DPRStatus.COMPLETED.value,
                "DPR creation completed successfully"
            )
            
            return {
                "success": True,
                "dpr_document": dpr_document,
                "compliance_check": compliance_result.get("compliance_check", {}),
                "risk_assessment": risk_result.get("risk_assessment", {}),
                "workflow_steps": [
                    "data_collection",
                    "financial_modeling",
                    "risk_assessment",
                    "document_generation",
                    "compliance_check"
                ]
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "orchestration_error",
                str(e),
                session_id
            )
            session_service.update_status(session_id, DPRStatus.FAILED)
            return {"success": False, "error": str(e)}

