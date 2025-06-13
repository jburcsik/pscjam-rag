"""
Example of integrating an MCP server with the GC Forms RAG API.
This demonstrates how to use the RAG system as a retrieval component
for a Model Context Protocol server.
"""
import requests
import json

class MCPServerIntegration:
    """
    A class that simulates an MCP server integrating with the RAG API.
    """
    
    def __init__(self, rag_endpoint="https://pscjam-rag-1.jesseburcsik.repl.co/query"):
        """Initialize with the RAG API endpoint."""
        self.rag_endpoint = rag_endpoint
        
    def get_context_from_rag(self, question):
        """
        Query the RAG system to get relevant context for a user question.
        
        Args:
            question (str): The user's question
            
        Returns:
            str: Context information from the RAG system, or None if not found
        """
        try:
            payload = {"query": question}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                self.rag_endpoint, 
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code != 200:
                print(f"Error querying RAG API: {response.status_code}")
                return None
                
            data = response.json()
            
            # Check if we got any results
            if not data.get('results') or len(data['results']) == 0:
                print("No relevant information found in the RAG system")
                return None
                
            # Compile context from all relevant results
            context = "Based on the GC Forms documentation:\n\n"
            
            for result in data['results']:
                # Add the text with its source information
                source = result.get('metadata', {}).get('source', 'Unknown source')
                similarity = result.get('similarity', 0) * 100
                
                if similarity >= 75:  # Only use highly relevant results
                    context += f"Information from {source} (relevance: {similarity:.1f}%):\n"
                    context += f"{result['text']}\n\n"
            
            return context
                
        except Exception as e:
            print(f"Error communicating with RAG API: {str(e)}")
            return None
    
    def process_mcp_request(self, mcp_request):
        """
        Process an MCP request by enriching it with RAG context.
        
        Args:
            mcp_request (dict): The MCP request containing user messages
            
        Returns:
            dict: The enriched MCP request
        """
        # Extract the last user message
        user_messages = [msg for msg in mcp_request.get('messages', []) 
                        if msg.get('role') == 'user']
        
        if not user_messages:
            print("No user messages found in the request")
            return mcp_request
            
        last_user_message = user_messages[-1]['content']
        
        # Get context from RAG system
        context = self.get_context_from_rag(last_user_message)
        
        # If we have relevant context, insert a system message before the last user message
        if context:
            # Find the position of the last user message
            messages = mcp_request['messages']
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get('role') == 'user':
                    last_user_index = i
                    break
            
            # Insert the system message with context
            system_message = {
                "role": "system",
                "content": context
            }
            
            # Insert just before the last user message
            enriched_messages = messages[:last_user_index]
            enriched_messages.append(system_message)
            enriched_messages.append(messages[last_user_index])
            enriched_messages.extend(messages[last_user_index + 1:])
            
            # Create the enriched request
            enriched_request = mcp_request.copy()
            enriched_request['messages'] = enriched_messages
            
            return enriched_request
        
        # If no context was found, return the original request
        return mcp_request

def example():
    """Example usage of the MCP server integration."""
    
    # Create an integration instance
    mcp_integration = MCPServerIntegration()
    
    # Sample MCP request
    mcp_request = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for GC Forms."},
            {"role": "user", "content": "How do I authenticate with the GC Forms API?"}
        ]
    }
    
    print("Original MCP request:")
    print(json.dumps(mcp_request, indent=2))
    
    # Enrich the request with RAG context
    enriched_request = mcp_integration.process_mcp_request(mcp_request)
    
    print("\nEnriched MCP request:")
    print(json.dumps(enriched_request, indent=2))
    
    print("\nThis enriched request can now be sent to your LLM provider.")

if __name__ == "__main__":
    example()
