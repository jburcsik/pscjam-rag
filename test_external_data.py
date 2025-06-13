"""
Script to test loading external data from Canada.ca Forms website and GitHub repo.
"""
from rag_engine import RAGEngine
from external_data import load_external_data

def main():
    """Test external data loading."""
    print("Initializing RAG engine...")
    rag_engine = RAGEngine()
    
    print("\nLoading external data...")
    docs_added = load_external_data(rag_engine, use_cache=True)
    
    print(f"\nAdded {docs_added} documents to the RAG engine.")
    
    print("\nTesting some sample queries on the loaded data:")
    test_queries = [
        "What is GC Forms?",
        "What security features are available in GC Forms?",
        "How do I create a form in the platform?",
        "What API endpoints are available in the Forms API?",
        "How do I authenticate with the Forms API?",
        "How do I submit a response to a form using the API?",
        "How do I retrieve form responses?"
    ]
    
    for query in test_queries:
        print(f"\n\nQuery: {query}")
        results = rag_engine.query(query)
        
        if results:
            print(f"Top {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n--- Result {i} (Similarity: {result['similarity']:.4f}) ---")
                # Print a shorter version of the text (first 200 chars)
                print(f"Text: {result['text'][:200]}...")
                print(f"Source: {result['metadata'].get('source', 'Unknown')}")
                print(f"URL/Path: {result['metadata'].get('url', result['metadata'].get('file_path', 'N/A'))}")
        else:
            print("No results found.")
    
    print("\nExternal data testing complete!")

if __name__ == "__main__":
    main()
