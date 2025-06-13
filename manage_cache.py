"""
Utility script to manage embedding cache.
"""
import os
import json
from vector_store import VectorStore
from rag_engine import RAGEngine
from external_data import load_external_data

def create_cache():
    """
    Create a fresh embeddings cache by processing all available data.
    """
    print("Creating fresh embeddings cache...")
    
    # Initialize RAG engine
    rag_engine = RAGEngine()
    
    # Load external data from Canada.ca Forms website and API docs
    print("Loading data from Canada.ca Forms website and API documentation...")
    docs_added = load_external_data(rag_engine, use_cache=True)
    print(f"Loaded {docs_added} documents")
    
    # Add some sample data too
    gc_forms_overview = """
    GC Forms is a powerful form creation and management system.
    It allows users to create custom forms for data collection,
    surveys, and feedback. Forms can be shared with specific users
    or made public. Results are automatically collected and can be
    exported in various formats.
    """
    
    print(f"Creating embedding for GC Forms overview document...")
    success = rag_engine.add_document(gc_forms_overview, {"type": "overview", "source": "GC Forms Documentation"})
    
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
    
    # Save embeddings to file
    cache_file = "embeddings_cache.json"
    print(f"Saving {len(rag_engine.vector_store.embeddings)} embeddings to {cache_file}")
    
    rag_engine.vector_store.save_embeddings(cache_file)
    print("Cache creation complete!")
    
    return len(rag_engine.vector_store.embeddings)

def inspect_cache(cache_file="embeddings_cache.json"):
    """
    Inspect an existing embeddings cache.
    """
    if not os.path.exists(cache_file):
        print(f"No cache file found at {cache_file}")
        return
    
    try:
        # Load the cache file
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # Display statistics
        print(f"\nCache Statistics for {cache_file}:")
        print(f"Total embeddings: {len(cache_data)}")
        
        # Count unique sources
        sources = {}
        for item in cache_data:
            source = item.get('metadata', {}).get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\nSources breakdown:")
        for source, count in sources.items():
            print(f"  - {source}: {count} embeddings")
        
        # Sample some text content
        if len(cache_data) > 0:
            print("\nSample text from first embedding:")
            sample_text = cache_data[0].get('text', '')
            print(f"  {sample_text[:200]}..." if len(sample_text) > 200 else sample_text)
        
        # Check embedding dimensions
        if len(cache_data) > 0 and 'embedding' in cache_data[0]:
            print(f"\nEmbedding dimensions: {len(cache_data[0]['embedding'])}")
        
        # Estimate file size
        cache_size_bytes = os.path.getsize(cache_file)
        print(f"\nCache file size: {cache_size_bytes / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"Error inspecting cache: {str(e)}")

def delete_cache(cache_file="embeddings_cache.json"):
    """
    Delete the embeddings cache file.
    """
    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
            print(f"Successfully deleted {cache_file}")
        except Exception as e:
            print(f"Error deleting cache file: {str(e)}")
    else:
        print(f"No cache file found at {cache_file}")

def main():
    """
    Main function to manage embedding cache.
    """
    print("Embeddings Cache Manager")
    print("=======================")
    
    while True:
        print("\nOptions:")
        print("1. Create new cache (process all data)")
        print("2. Inspect existing cache")
        print("3. Delete cache file")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            create_cache()
        elif choice == '2':
            inspect_cache()
        elif choice == '3':
            confirm = input("Are you sure you want to delete the cache? (y/n): ")
            if confirm.lower() == 'y':
                delete_cache()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
