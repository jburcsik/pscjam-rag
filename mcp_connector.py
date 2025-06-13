"""
Complete client code for connecting an MCP server to the GC Forms RAG API.
This is a ready-to-use example that can be dropped into any Python-based MCP server.
"""

import requests
import json
import os
from typing import List, Dict, Any, Optional

# Configuration
RAG_API_ENDPOINT = "https://pscjam-rag-1.jesseburcsik.repl.co/query"

class GCFormsRagConnector:
    """
    Connector for enriching LLM prompts with GC Forms documentation from the RAG API.
    """
    
    def __init__(self, api_endpoint: str = RAG_API_ENDPOINT):
        """
        Initialize the connector.
        
        Args:
            api_endpoint: URL of the RAG API endpoint
        """
        self.api_endpoint = api_endpoint
    
    def get_relevant_context(self, query: str, top_k: int = 3) -> Optional[str]:
        """
        Get relevant documentation context for a given query.
        
        Args:
            query: The user's question about GC Forms
            top_k: Maximum number of relevant documents to retrieve
            
        Returns:
            Formatted context string or None if no relevant information found
        """
        # Send query to RAG API
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "query": query
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"Error: RAG API returned status code {response.status_code}")
                return None
            
            result = response.json()
            
            if not result.get("results") or len(result["results"]) == 0:
                print("No relevant information found in the RAG system")
                return None
            
            # Format the context with the retrieved information
            context = "Here is relevant information about GC Forms:\n\n"
            
            for i, doc in enumerate(result["results"], 1):
                similarity = doc.get("similarity", 0)
                
                # Only include highly relevant results
                if similarity < 0.7:
                    continue
                
                # Add metadata if available
                source = doc.get("metadata", {}).get("source", "Documentation")
                title = doc.get("metadata", {}).get("title", f"Document {i}")
                
                context += f"[From {source}]: {doc['text']}\n\n"
            
            return context
            
        except Exception as e:
            print(f"Error querying RAG API: {str(e)}")
            return None
    
    def enrich_mcp_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enrich MCP messages with relevant GC Forms documentation.
        
        Args:
            messages: List of MCP message dictionaries
            
        Returns:
            Enriched list of messages
        """
        if not messages:
            return messages
        
        # Find the last user message
        user_message = None
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                user_message = messages[i]["content"]
                user_message_idx = i
                break
        
        if not user_message:
            return messages
        
        # Get context from RAG API
        context = self.get_relevant_context(user_message)
        
        if not context:
            return messages
        
        # Insert system message with context before the last user message
        context_message = {
            "role": "system",
            "content": context
        }
        
        enriched_messages = messages.copy()
        # Insert right before the last user message to maintain context flow
        enriched_messages.insert(user_message_idx, context_message)
        
        return enriched_messages

# Example usage
if __name__ == "__main__":
    # Sample MCP messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How do I authenticate with the GC Forms API?"}
    ]
    
    # Create connector
    connector = GCFormsRagConnector()
    
    # Enrich messages with context
    enriched_messages = connector.enrich_mcp_messages(messages)
    
    print("Original messages:")
    print(json.dumps(messages, indent=2))
    
    print("\nEnriched messages:")
    print(json.dumps(enriched_messages, indent=2))
    
    # Shows how to use with your own LLM provider (OpenAI in this example)
    print("\nExample of sending to OpenAI:")
    print("""
    import openai
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=enriched_messages
    )
    
    print(response.choices[0].message["content"])
    """)
