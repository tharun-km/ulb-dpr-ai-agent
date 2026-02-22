"""
Document Generation Agent - Level 1
Assembles DPR sections and generates final document with sector-specific templates.
"""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent
from src.models.dpr_schema import DPRDocument, Sector
from src.services.memory_service.working_memory import working_memory
from src.services.observability.logging import agent_logger


class DocumentGeneratorAgent(BaseAgent):
    """
    Document generation agent that assembles DPR sections.
    Uses sector-specific templates.
    """
    
    def __init__(self):
        super().__init__(
            name="document_generator",
            description="Assembles DPR sections and generates final document"
        )
    
    async def execute(
        self,
        session_id: str,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate DPR document."""
        try:
            ulb_metadata = input_data.get("ulb_metadata", {})
            financial_model = input_data.get("financial_model", {})
            risk_assessment = input_data.get("risk_assessment", {})
            sector = Sector(input_data.get("sector", "water_supply"))
            collected_data = input_data.get("collected_data", {})
            
            # Generate document sections using LLM
            prompt = f"""
            Generate a Detailed Project Report (DPR) for a {sector.value} PPP project.
            
            ULB: {ulb_metadata.get('name', 'Unknown')}
            Sector: {sector.value}
            
            Include the following sections:
            1. Executive Summary
            2. Project Description
            3. Technical Specifications
            4. Financial Model
            5. Risk Assessment
            6. Implementation Plan
            
            Make it comprehensive and suitable for government approval.
            """
            
            response = self._generate_response(prompt, session_id)
            
            # Create DPR document structure
            dpr_document = {
                "ulb_metadata": ulb_metadata,
                "sector": sector.value,
                "project_title": f"{sector.value.replace('_', ' ').title()} Project - {ulb_metadata.get('name', 'ULB')}",
                "executive_summary": response[:500] + "...",  # Extract from response
                "project_description": response,
                "technical_specifications": collected_data.get("existing_infrastructure", {}),
                "financial_model": financial_model,
                "risk_assessment": risk_assessment,
                "implementation_plan": {
                    "timeline": "24 months",
                    "phases": ["Planning", "Procurement", "Implementation", "Operations"]
                },
                "status": "document_generation"
            }
            
            # Store in working memory
            working_memory.store_intermediate_result(
                session_id,
                "dpr_document",
                dpr_document
            )
            
            self._log_decision(
                "Generated DPR document",
                f"Document created for {sector.value} sector",
                0.90,
                session_id
            )
            
            return {
                "success": True,
                "dpr_document": dpr_document,
                "document_text": response
            }
        
        except Exception as e:
            agent_logger.log_error(
                self.name,
                "document_generation_error",
                str(e),
                session_id
            )
            return {"success": False, "error": str(e)}


