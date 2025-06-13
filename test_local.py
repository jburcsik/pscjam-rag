#!/usr/bin/env python3
"""
Test script for the local RAG API
"""
import requests
import json
import sys

def test_local_endpoint(endpoint_path="query", query="What is GC Forms?"):
    """
    Test a specific endpoint on the local service
    
    Args:
        endpoint_path: The path part of the URL (e.g., "query" or "api/mcp")
        query: The question to ask
    """
    base_url = "http://localhost:5001"
    url = f"{base_url}/{endpoint_path}"
    
    print(f"Testing connection to {base_url}...")
    try:
        # First check if local server is responding
        print(f"Checking if local server is online...")
        health_check = requests.get(base_url, timeout=5)
        print(f"Server status code: {health_check.status_code}")
    except Exception as e:
        print(f"ERROR: Could not connect to local server: {str(e)}")
        print("Is your Flask application running on port 5001?")
        return False
    
    print(f"\nSending query '{query}' to {url}")
    
    payload = {
        "query": query
    }
    
    # Add request_type for MCP endpoint
    if endpoint_path == "api/mcp":
        payload["request_type"] = "user_query"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nResponse data:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    # Test the main query endpoint by default
    endpoint = "query"
    query = "What is GC Forms?"
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        endpoint = sys.argv[1]
    
    if len(sys.argv) > 2:
        query = sys.argv[2]
    
    print("=" * 50)
    print(f"Testing Local deployment of GC Forms RAG API")
    print(f"Base URL: http://localhost:5001")
    print(f"Testing endpoint: /{endpoint}")
    print(f"Query: '{query}'")
    print("=" * 50)
    
    success = test_local_endpoint(endpoint, query)
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n⚠️ Test encountered issues. Check the logs above.")
