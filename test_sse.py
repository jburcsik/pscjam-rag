#!/usr/bin/env python3
"""
Test script for the streaming SSE endpoint
"""
import requests
import json
import sys
import time

def test_sse_endpoint(query="What is GC Forms?"):
    """
    Test the SSE endpoint manually
    
    Args:
        query: The question to ask
    """
    base_url = "http://localhost:5001"
    endpoint_path = "api/mcp/stream"
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
    
    print(f"\nInitiating streaming request with query: '{query}' to {url}")
    
    payload = {
        "request_type": "user_query",
        "query": query
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send the POST request and get a streaming response
        print("\nSending SSE request...")
        
        with requests.post(url, json=payload, stream=True, headers=headers) as response:
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                print("\nStreaming events:")
                print("-" * 50)
                
                # Process the streaming response
                buffer = ""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        text = chunk.decode('utf-8')
                        buffer += text
                        
                        # Process complete events
                        events = buffer.split("\n\n")
                        buffer = events.pop()  # Keep last incomplete event in buffer
                        
                        for event in events:
                            if event.strip():
                                print_sse_event(event)
                                
                print("-" * 50)
                print("Stream completed or connection closed")
                return True
            else:
                print(f"Error response: {response.text}")
                return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False

def print_sse_event(event_text):
    """Print an SSE event in a readable format."""
    lines = event_text.split("\n")
    event_type = None
    event_data = None
    
    for line in lines:
        if line.startswith("event:"):
            event_type = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            event_data = line.split(":", 1)[1].strip()
    
    if event_type:
        print(f"Event: {event_type}")
        if event_data:
            try:
                data = json.loads(event_data)
                print(f"Data: {json.dumps(data, indent=2)}")
            except:
                print(f"Data: {event_data}")
        print()  # Empty line for readability

if __name__ == "__main__":
    # Get query from command line args or use default
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What is GC Forms?"
    
    print("=" * 70)
    print(f"Testing SSE Streaming Endpoint")
    print(f"Query: '{query}'")
    print("=" * 70)
    
    test_sse_endpoint(query)
