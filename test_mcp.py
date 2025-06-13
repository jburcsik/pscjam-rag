#!/usr/bin/env python3
"""
Test script for the MCP endpoint of the RAG API
"""
import requests
import json
import sys

def test_mcp_endpoint(query="What is GC Forms?"):
    """
    Test the MCP endpoint on the local service
    
    Args:
        query: The question to ask
    """
    base_url = "http://localhost:5001"
    endpoint_path = "api/mcp"
    url = f"{base_url}/{endpoint_path}"
    
    print(f"Testing connection to {base_url}...")
    try:
        # First check if local server is responding
        print(f"Checking if local server is online...")
        health_check = requests.get(f"{base_url}/health", timeout=5)
        print(f"Server status code: {health_check.status_code}")
        print(f"Health check response: {health_check.json()}")
    except Exception as e:
        print(f"ERROR: Could not connect to local server: {str(e)}")
        print("Is your Flask application running on port 5001?")
        return False
    
    print(f"\nSending query '{query}' to {url}")
    
    payload = {
        "request_type": "user_query",
        "query": query
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("\nMaking request to MCP endpoint...")
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status code: {response.status_code}")
        
        # Print raw response for debugging
        print("\nRaw response:")
        print(response.text)
        
        if response.status_code == 200:
            data = response.json()
            print("\nFormatted response data:")
            print(json.dumps(data, indent=2))
            
            # Check if we got a meaningful response
            if data.get('response'):
                response_length = len(data['response'])
                print(f"\nResponse length: {response_length} characters")
                if response_length < 50:
                    print("⚠️ Warning: Response seems very short, may not be useful")
                elif "couldn't find any information" in data['response'].lower():
                    print("⚠️ Warning: Generic 'no information' response received")
                else:
                    print("✅ Response appears to be substantive")
            else:
                print("⚠️ No 'response' field in the response data")
                
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def compare_endpoints(query="How do I create a form?"):
    """
    Compare results from both /query and /api/mcp endpoints
    
    Args:
        query: The question to ask both endpoints
    """
    base_url = "http://localhost:5001"
    
    print(f"Comparing endpoints with query: '{query}'")
    
    # Test the regular query endpoint first
    query_url = f"{base_url}/query"
    query_payload = {"query": query}
    
    print("\n1. Testing /query endpoint...")
    query_response = requests.post(
        query_url,
        headers={"Content-Type": "application/json"},
        json=query_payload
    )
    
    if query_response.status_code == 200:
        query_data = query_response.json()
        result_count = len(query_data.get('results', []))
        print(f"✅ Query endpoint returned {result_count} results")
        if result_count > 0:
            top_similarity = query_data['results'][0].get('similarity', 0)
            print(f"   Top result similarity: {top_similarity:.2f}")
    else:
        print(f"❌ Query endpoint failed with status {query_response.status_code}")
    
    # Now test the MCP endpoint
    mcp_url = f"{base_url}/api/mcp"
    mcp_payload = {
        "request_type": "user_query",
        "query": query
    }
    
    print("\n2. Testing /api/mcp endpoint...")
    mcp_response = requests.post(
        mcp_url,
        headers={"Content-Type": "application/json"},
        json=mcp_payload
    )
    
    if mcp_response.status_code == 200:
        mcp_data = mcp_response.json()
        mcp_response_text = mcp_data.get('response', '')
        print(f"✅ MCP endpoint returned a response ({len(mcp_response_text)} chars)")
        if mcp_response_text:
            print(f"   Preview: {mcp_response_text[:100]}...")
    else:
        print(f"❌ MCP endpoint failed with status {mcp_response.status_code}")
    
    print("\n3. Comparison Summary:")
    if query_response.status_code == 200 and mcp_response.status_code == 200:
        query_results = query_response.json().get('results', [])
        mcp_text = mcp_response.json().get('response', '')
        
        # Check if any query results appear in the MCP response
        shared_content = False
        if query_results and mcp_text:
            for result in query_results:
                result_text = result.get('text', '')
                if result_text and result_text[:20] in mcp_text:
                    shared_content = True
                    break
        
        if shared_content:
            print("✅ The MCP response contains content from the query results")
        else:
            print("⚠️ The MCP response doesn't seem to use content from the query results")
    
    return True

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        # Run comparison test with optional query
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "How do I create a form?"
        compare_endpoints(query)
    else:
        # Run regular MCP test with optional query
        query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is GC Forms?"
        
        print("=" * 50)
        print(f"Testing MCP Endpoint of GC Forms RAG API")
        print(f"Base URL: http://localhost:5001")
        print(f"Query: '{query}'")
        print("=" * 50)
        
        success = test_mcp_endpoint(query)
        
        if success:
            print("\n✅ MCP test completed!")
            print("\nTo compare both endpoints with the same query, run:")
            print(f"python {sys.argv[0]} compare \"your query here\"")
        else:
            print("\n⚠️ MCP test encountered issues. Check the logs above.")
