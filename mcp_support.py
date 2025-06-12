"""
Enhanced RAG Engine for supporting an MCP server.
This module extends the basic RAG engine to support:
1. Informational queries - answering questions about docs
2. Code generation - helping write code based on documentation
"""
from rag_engine import RAGEngine
import requests
import json
import os
from api_secrets import get_api_key

class MCPSupportEngine:
    """
    Enhanced RAG system to support an MCP server with information
    retrieval and code generation capabilities.
    """
    
    def __init__(self):
        """Initialize the MCP Support Engine."""
        self.rag_engine = RAGEngine()
        self.api_key = get_api_key()
    
    def add_document(self, text, metadata=None):
        """Add document to the knowledge base."""
        return self.rag_engine.add_document(text, metadata)
    
    def inform_user(self, query_text, max_results=3):
        """
        Retrieve relevant information to answer a user's question.
        
        Args:
            query_text (str): The user's question
            max_results (int): Maximum number of results to include
            
        Returns:
            dict: Response with answer and retrieved context
        """
        # Get relevant information using our RAG system
        results = self.rag_engine.query(query_text)
        
        # Keep only the top results
        top_results = results[:max_results] if results else []
        
        # Construct the context from retrieved documents
        context = ""
        for result in top_results:
            context += f"\n\nDocument (relevance {result['similarity']:.2f}):\n{result['text']}\n"
        
        # If we have results, provide a direct answer
        if top_results:
            return {
                "type": "information",
                "query": query_text,
                "results": top_results,
                "context": context
            }
        else:
            return {
                "type": "information",
                "query": query_text,
                "results": [],
                "message": "No relevant information found."
            }
    
    def generate_code(self, requirements, language="python"):
        """
        Generate code based on requirements and retrieved documentation.
        
        Args:
            requirements (str): Description of what the code should do
            language (str): Programming language to generate
            
        Returns:
            dict: Response with generated code and context
        """
        # First, get relevant documentation as context
        results = self.rag_engine.query(requirements)
        top_results = results[:2] if results else []
        
        # Construct the context from retrieved documents
        context = ""
        for result in top_results:
            context += f"\n\nDocumentation:\n{result['text']}\n"
        
        # For a real implementation, this would call an LLM API
        # This is a placeholder that would be replaced with actual code generation
        return {
            "type": "code_generation",
            "requirements": requirements,
            "language": language,
            "context_used": context,
            "message": "This would generate code based on the requirements and documentation."
        }
