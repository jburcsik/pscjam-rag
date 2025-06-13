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
    
    def load_embeddings(self, file_path="mcp_embeddings_cache.json"):
        """Load embeddings from cache file."""
        return self.rag_engine.vector_store.load_embeddings(file_path)
    
    def save_embeddings(self, file_path="mcp_embeddings_cache.json"):
        """Save embeddings to cache file."""
        return self.rag_engine.vector_store.save_embeddings(file_path)
    
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
    
    def process_mcp_request(self, data):
        """
        Process an MCP request and generate a response based on the request type.
        
        Args:
            data (dict): The request data from the API containing request_type and query
            
        Returns:
            dict: Response with appropriate data based on request type
        """
        print(f"Processing MCP request with data: {data}")
        
        # Handle different types of requests
        request_type = data.get('request_type')
        
        if request_type == 'user_query':
            query = data.get('query')
            if not query:
                return {"error": "No query provided in request"}
            
            print(f"Processing user query: {query}")
            
            # Force a re-query using the same vector store as the RAG engine
            # since the rag_engine.query method might have internal state
            print(f"Directly searching vector store with query: {query}")
            embedding = self.rag_engine.vector_store.create_embedding(query)
            results = self.rag_engine.vector_store.search(embedding)
            print(f"MCP query found {len(results)} results")
            
            if not results:
                print("No results found for MCP query")
                return {
                    "query": query,
                    "response": "I couldn't find any information related to your query.",
                    "sources": []
                }
            
            # Format source references
            sources = []
            for i, result in enumerate(results[:3]):  # Use top 3 results
                source = result.get('metadata', {}).get('source', 'Documentation')
                sources.append(f"{source} (relevance: {result['similarity']:.2f})")
            
            print(f"Sources for MCP response: {sources}")
            
            # Create a human-like response based on the results
            response = self._generate_response_from_context(query, results)
            print(f"Generated MCP response: {response[:100]}...")
            
            return {
                "query": query,
                "response": response,
                "sources": ", ".join(sources)
            }
            
        elif request_type == 'code_generation':
            requirements = data.get('requirements', '')
            language = data.get('language', 'python')
            
            return self.generate_code(requirements, language)
            
        else:
            return {"error": f"Unknown request type: {request_type}"}
    
    def _generate_response_from_context(self, query, results):
        """
        Generate a human-like response based on retrieved results.
        
        Args:
            query (str): The user's query
            results (list): The results from the RAG engine
            
        Returns:
            str: A human-like response
        """
        if not results:
            return "I don't have information about that."
        
        try:    
            # Extract the most relevant result
            top_result = results[0]['text']
            
            # Format a response
            response = f"Based on the GC Forms documentation, {top_result}\n\n"
            
            # Add information from other results if they offer something different
            if len(results) > 1:
                for result in results[1:3]:  # Add info from next 2 results
                    # Add only if it adds new information (simple heuristic)
                    if len(result['text']) > 20 and result['text'] not in response:
                        response += f"Additionally, {result['text']}\n\n"
            
            return response.strip()
        except Exception as e:
            print(f"Error generating response from context: {str(e)}")
            print(f"Results were: {results}")
            
            # Fallback response that still provides value
            text_list = [r.get('text', '') for r in results if isinstance(r, dict) and 'text' in r]
            if text_list:
                combined_text = ' '.join(text_list[:2])  # Use first 2 results
                return f"Here's what I found about GC Forms: {combined_text}"
            else:
                return "I found some information about GC Forms but couldn't format it properly."
