"""
Test script to verify that the OpenAI completions integration works.
"""
import os
from mcp_support import MCPSupportEngine
import json

def test_openai_completion():
    """Test the OpenAI completions integration."""
    print("Initializing MCP Support Engine...")
    mcp_engine = MCPSupportEngine()
    
    # Load cached embeddings
    print("Loading embeddings from cache...")
    cache_loaded = mcp_engine.load_embeddings()
    print(f"Cache loaded: {cache_loaded}")
    
    if not cache_loaded or len(mcp_engine.rag_engine.vector_store.embeddings) == 0:
        print("Error: No embeddings found in cache. Please run the app first to initialize the cache.")
        return
    
    # Test query
    query = "What are the key features of GC Forms?"
    print(f"Testing query: {query}")
    
    # Search for documents
    embedding = mcp_engine.rag_engine.vector_store.create_embedding(query)
    results = mcp_engine.rag_engine.vector_store.search(embedding, top_k=3)
    
    print(f"Found {len(results)} results")
    for i, result in enumerate(results):
        print(f"Result {i+1}: Similarity {result['similarity']:.4f}")
        print(f"Preview: {result['text'][:100]}...")
    
    # Generate response using OpenAI completions
    print("\nGenerating response using OpenAI completions...")
    response = mcp_engine._generate_response_from_context(query, results)
    
    print("\n=== Generated Response ===")
    print(response)
    print("========================")
    
    # Test MCP request
    print("\nTesting MCP request processing...")
    mcp_request = {
        "request_type": "user_query",
        "query": query
    }
    
    mcp_response = mcp_engine.process_mcp_request(mcp_request)
    print("\n=== MCP Response ===")
    print(json.dumps(mcp_response, indent=2))
    print("===================")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_openai_completion()
