"""
Main application file to demonstrate the RAG system.
"""
from rag_engine import RAGEngine

def main():
    """Main function to demonstrate the RAG system."""
    # Initialize our RAG engine
    rag_engine = RAGEngine()
    
    # Add some mock data for 'GC Forms'
    print("Adding mock GC Forms data to the system...")
    
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
    
    # Let's try a simple query
    print("\nTesting a simple query...")
    query = "What are the main features of GC Forms?"
    results = rag_engine.query(query)
    
    print(f"Query: {query}")
    
    if results:
        print("\nResults:")
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} (Similarity: {result['similarity']:.4f}) ---")
            print(f"Text: {result['text']}")
            print(f"Metadata: {result['metadata']}")
    else:
        print("\nNo results found.")
    
    print("\nInitial RAG system setup is complete!")

if __name__ == "__main__":
    main()
