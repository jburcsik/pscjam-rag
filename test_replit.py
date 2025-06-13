#!/usr/bin/env python3
"""
Test script for the GC Forms RAG API on Replit
"""
import requests
import json
import sys
import time

def test_replit_endpoint(endpoint_path="query", query="What is GC Forms?"):
    """
    Test a specific endpoint on the Replit service
    
    Args:
        endpoint_path: The path part of the URL (e.g., "query" or "api/mcp")
        query: The question to ask
    """
    base_url = "https://pscjam-rag-1.jesseburcsik.repl.co"
    url = f"{base_url}/{endpoint_path}"
    
    print(f"Testing connection to {base_url}...")
    try:
        # First check if Replit is even responding
        print(f"Checking if Replit is online...")
        health_check = requests.get(base_url, timeout=5)
        print(f"Replit status code: {health_check.status_code}")
    except Exception as e:
        print(f"ERROR: Could not connect to Replit: {str(e)}")
        print("The Replit service might be asleep or unavailable.")
        return
    
    payload = {
        "query": query
    }
    
    # Add request_type for MCP endpoint
    if endpoint_path == "api/mcp":
        payload["request_type"] = "user_query"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing endpoint: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("Sending request...")
    
    try:
        print("Attempting connection - this might take up to 30 seconds if Replit is sleeping...")
        start_time = time.time()
        
        response = requests.post(
            url, 
            headers=headers, 
            data=json.dumps(payload),
            timeout=30  # 30 second timeout
        )
        
        elapsed_time = time.time() - start_time
        print(f"Connection completed in {elapsed_time:.2f} seconds")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("Response data:")
                print(json.dumps(data, indent=2))
                return True
            except json.JSONDecodeError:
                print("Error decoding JSON response")
                print(f"Raw response: {response.text}")
                return False
        else:
            print(f"Error response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("\n⚠️ Connection timed out after 30 seconds")
        print("This likely means your Replit application is in sleep mode.")
        print("Visit your Replit URL directly to wake it up: https://pscjam-rag-1.jesseburcsik.repl.co")
        return False
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Connection failed - could not reach Replit server")
        print("This might be because:")
        print("1. The Replit project is not running")
        print("2. There's a network issue")
        print("3. The Replit URL has changed")
        return False
    except requests.exceptions.RequestException as e:
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
    print(f"Testing Replit deployment of GC Forms RAG API")
    print(f"Base URL: https://pscjam-rag-1.jesseburcsik.repl.co")
    print(f"Testing endpoint: /{endpoint}")
    print(f"Query: '{query}'")
    print("=" * 50)
    
    print("\nNote: If your Replit deployment hasn't been accessed recently,")
    print("it might take 15-30 seconds to 'wake up' from sleep mode.\n")
    
    print("Starting test...")
    success = test_replit_endpoint(endpoint, query)
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n⚠️ Test encountered issues. Check the logs above.")
        
    print("\nIf the Replit service is not responding, you may need to:")
    print("1. Visit https://replit.com/@jesseburcsik/pscjam-rag-1")
    print("2. Make sure the project is running")
    print("3. Check that your app is properly deployed")
    
    print("\nTo test local development instead, you can use:")
    print("curl -X POST http://localhost:5001/query -H \"Content-Type: application/json\" -d '{\"query\":\"What is GC Forms?\"}'")
