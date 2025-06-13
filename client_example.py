"""
Example client for the GC Forms RAG API.
"""
import requests
import json

def query_rag_api(question):
    """
    Send a query to the RAG API and return the results.
    
    Args:
        question (str): The question to ask about GC Forms
        
    Returns:
        dict: The API response
    """
    url = "https://pscjam-rag-1.jesseburcsik.repl.co/query"
    payload = {"query": question}
    headers = {"Content-Type": "application/json"}
    
    try:
        print(f"Sending query: '{question}'")
        print(f"To endpoint: {url}")
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying the RAG API: {e}")
        return None

def display_results(data):
    """
    Display the results from the RAG API in a readable format.
    
    Args:
        data (dict): The API response
    """
    if not data or "results" not in data:
        print("No results returned from the API.")
        return
    
    print("\n=== RESULTS ===\n")
    
    for i, result in enumerate(data["results"], 1):
        print(f"Result {i} (Similarity: {result['similarity']:.4f})")
        print("-" * 50)
        print(f"Text: {result['text']}")
        
        if "metadata" in result:
            print("\nMetadata:")
            for key, value in result["metadata"].items():
                print(f"  {key}: {value}")
        
        print("\n" + "=" * 50 + "\n")

def main():
    """
    Main function to demonstrate the RAG API client.
    """
    print("GC Forms RAG API Client")
    print("======================")
    
    while True:
        print("\nEnter your question about GC Forms (or 'exit' to quit):")
        question = input("> ")
        
        if question.lower() in ("exit", "quit", "q"):
            break
        
        if not question.strip():
            continue
        
        results = query_rag_api(question)
        display_results(results)

if __name__ == "__main__":
    main()
