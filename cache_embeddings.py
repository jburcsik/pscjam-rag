"""
Script to save and load embeddings to improve performance.
"""
import json
import os
from vector_store import VectorStore
from rag_engine import RAGEngine

def save_embeddings(vector_store, file_path="embeddings_cache.json"):
    """
    Save embeddings to a cache file.
    
    Args:
        vector_store: The VectorStore instance
        file_path: Path to save the embeddings cache
    """
    print(f"Saving {len(vector_store.embeddings)} embeddings to {file_path}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(vector_store.embeddings, f)
    
    print(f"Successfully saved embeddings cache.")

def load_embeddings(vector_store, file_path="embeddings_cache.json"):
    """
    Load embeddings from a cache file.
    
    Args:
        vector_store: The VectorStore instance to load into
        file_path: Path to the embeddings cache
        
    Returns:
        bool: True if embeddings were successfully loaded
    """
    if not os.path.exists(file_path):
        print(f"No embeddings cache found at {file_path}")
        return False
    
    try:
        print(f"Loading embeddings from {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            vector_store.embeddings = json.load(f)
        
        print(f"Successfully loaded {len(vector_store.embeddings)} embeddings.")
        return True
    except Exception as e:
        print(f"Error loading embeddings: {str(e)}")
        return False

def main():
    """
    Example of using the cache functionality.
    """
    # Initialize RAG engine
    rag = RAGEngine()
    
    # Check if we have cached embeddings
    cache_loaded = load_embeddings(rag.vector_store)
    
    # If not, load data and create embeddings
    if not cache_loaded:
        print("Loading and embedding documents...")
        from external_data import load_external_data
        load_external_data(rag)
        
        # Save for next time
        save_embeddings(rag.vector_store)
    
    # Test a query
    query = "How do I authenticate with the Forms API?"
    print(f"\nQuery: {query}")
    results = rag.query(query)
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (Similarity: {result['similarity']:.4f})")
        print(f"Source: {result['metadata'].get('source', 'Unknown')}")
        print(f"URL: {result['metadata'].get('url', 'N/A')}")
        
if __name__ == "__main__":
    main()
