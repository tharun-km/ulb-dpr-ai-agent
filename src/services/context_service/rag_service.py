"""
RAG (Retrieval-Augmented Generation) service for government guidelines.
"""
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from src.utils.config import config


class RAGService:
    """
    RAG service for retrieving relevant government guidelines and standards.
    Helps agents access up-to-date compliance requirements.
    """
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.documents: List[Document] = []
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embeddings model."""
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=config.gemini_api_key
            )
        except Exception as e:
            # Fallback if embeddings not available
            print(f"Warning: Could not initialize embeddings: {e}")
            self.embeddings = None
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the RAG knowledge base."""
        try:
            doc_objects = [
                Document(
                    page_content=doc.get("content", ""),
                    metadata=doc.get("metadata", {})
                )
                for doc in documents
            ]
            self.documents.extend(doc_objects)
            
            if self.embeddings and len(self.documents) > 0:
                self.vector_store = FAISS.from_documents(
                    self.documents,
                    self.embeddings
                )
            return True
        except Exception as e:
            print(f"Error adding documents to RAG: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        if not self.vector_store:
            # Fallback to simple text search
            return self._simple_search(query, k)
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in results
            ]
        except Exception as e:
            print(f"Error in RAG search: {e}")
            return self._simple_search(query, k)
    
    def _simple_search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Simple text-based search fallback."""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            if query_lower in content_lower:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": 0.5  # Default score for simple search
                })
        
        return results[:k]
    
    def get_guidelines(self, topic: str, sector: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get relevant guidelines for a topic and optional sector."""
        query = f"{topic}"
        if sector:
            query += f" {sector} sector"
        
        return self.search(query, k=5)


# Global RAG service instance
rag_service = RAGService()


