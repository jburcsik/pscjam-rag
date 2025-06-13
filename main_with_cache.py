"""
Main application file with embedding cache for the RAG system.
"""
from rag_engine import RAGEngine
import os
from external_data import load_external_data

def main():
    """Main function to demonstrate the RAG system with caching."""
    # Initialize our RAG engine
    print("Initializing RAG engine...")
    rag_engine = RAGEngine()
    
    # Cache file path
    embeddings_cache = "embeddings_cache.json"
    
    # Try to load cached embeddings
    print("Checking for cached embeddings...")
    cache_loaded = False
    
    if os.path.exists(embeddings_cache):
        print(f"Found embeddings cache at {embeddings_cache}")
        cache_loaded = rag_engine.vector_store.load_embeddings(embeddings_cache)
    
    # If no cache or failed to load, create new embeddings
    if not cache_loaded:
        print("No cache found or failed to load. Creating new embeddings...")
        
        # Add both sample data and external data
        print("Adding sample GC Forms data to the system...")
        
        # Sample 1: GC Forms Overview
        gc_forms_overview = """
        GC Forms is a powerful form creation and management system.
        It allows users to create custom forms for data collection,
        surveys, and feedback. Forms can be shared with specific users
        or made public. Results are automatically collected and can be
        exported in various formats.
        """
        
        print(f"Creating embedding for GC Forms overview document...")
        success = rag_engine.add_document(gc_forms_overview, {"type": "overview", "source": "GC Forms Documentation"})
        print(f"Added GC Forms overview document: {'Success' if success else 'Failed'}")
        
        # Sample 2: GC Forms Features
        gc_forms_features = """
        Key features of GC Forms include:
        1. Drag-and-drop form builder
        2. Multiple question types (text, multiple choice, checkboxes)
        3. Conditional logic for dynamic forms
        4. File upload capabilities
        5. Automatic data validation
        6. Real-time collaboration
        7. Response analytics and visualization
        8. Integration with other systems via APIs
        """
        
        print(f"Creating embedding for GC Forms features document...")
        success = rag_engine.add_document(gc_forms_features, {"type": "features", "source": "GC Forms Documentation"})
        print(f"Added GC Forms features document: {'Success' if success else 'Failed'}")
        
        # Load external data from Canada.ca Forms website and API docs
        print("Loading external data from Canada.ca Forms website and API documentation...")
        docs_added = load_external_data(rag_engine)
        print(f"Added {docs_added} external documents")
        
        # Save embeddings for future use
        print("Saving embeddings to cache...")
        rag_engine.vector_store.save_embeddings(embeddings_cache)
    
    # Run some test queries
    print("\nTesting queries with our RAG system...")
    
    test_queries = [
        "What are the main features of GC Forms?",
        "How do I use the Forms API?",
        "What authentication methods are supported by the API?",
        "How can I create a new form using the website?"
    ]
    
    for query in test_queries:
        print(f"\n\nQuery: {query}")
        results = rag_engine.query(query)
        
        if results:
            print("\nResults:")
            for i, result in enumerate(results, 1):
                print(f"\n--- Result {i} (Similarity: {result['similarity']:.4f}) ---")
                source = result['metadata'].get('source', 'Unknown source')
                print(f"Source: {source}")
                print(f"Text snippet: {result['text'][:200]}...")
        else:
            print("\nNo results found.")
    
    print("\nRAG system with caching is complete!")

if __name__ == "__main__":
    main()
