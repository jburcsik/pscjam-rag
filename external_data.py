"""
External data integration module for the RAG system.
"""
import os
import json
from web_scraper import scrape_canada_forms_website
# For API documentation, we have a JSON file directly
# Uncomment the following line if you want to scrape instead
# from api_doc_scraper import scrape_api_documentation

def load_external_data(rag_engine, use_cache=True):
    """
    Load external data into the RAG system from both the Canada.ca Forms website
    and the Forms API documentation site.
    
    Args:
        rag_engine: The RAG engine to load data into
        use_cache: Whether to use cached data files if they exist
        
    Returns:
        int: Number of documents added
    """
    docs_added = 0
    total_chunks = 0
    
    # 1. Load website data
    website_data_file = "canada_forms_content.json"
    
    if use_cache and os.path.exists(website_data_file):
        # Use cached data
        print(f"Loading website data from cache: {website_data_file}")
        try:
            with open(website_data_file, 'r', encoding='utf-8') as f:
                website_documents = json.load(f)
        except Exception as e:
            print(f"Error loading cached website data: {str(e)}")
            website_documents = []
    else:
        # Scrape fresh data
        print("Scraping website data from Canada.ca Forms website...")
        website_documents = scrape_canada_forms_website(max_pages=30)
    
    # Add website documents to the RAG engine
    print(f"Adding {len(website_documents)} website documents to the RAG engine...")
    for doc in website_documents:
        try:
            success = rag_engine.add_document(doc["text"], doc["metadata"])
            if success:
                docs_added += 1
                # Count chunks based on add_document return value if available
                if isinstance(success, int):
                    total_chunks += success
                else:
                    total_chunks += 1
        except Exception as e:
            print(f"Error adding website document: {str(e)}")
    
    # 2. Load API documentation data
    api_docs_file = "api_docs_content.json"
    
    if os.path.exists(api_docs_file):
        # Load API documentation from file
        print(f"Loading API documentation data from file: {api_docs_file}")
        try:
            with open(api_docs_file, 'r', encoding='utf-8') as f:
                api_documents = json.load(f)
            print(f"Successfully loaded {len(api_documents)} API documentation entries")
        except Exception as e:
            print(f"Error loading API documentation data: {str(e)}")
            api_documents = []
    else:
        print(f"Warning: API documentation file {api_docs_file} not found")
        api_documents = []
    
    # Add API documentation to the RAG engine
    print(f"Adding {len(api_documents)} API documentation documents to the RAG engine...")
    for doc in api_documents:
        try:
            success = rag_engine.add_document(doc["text"], doc["metadata"])
            if success:
                docs_added += 1
                # Count chunks based on add_document return value if available
                if isinstance(success, int):
                    total_chunks += success
                else:
                    total_chunks += 1
        except Exception as e:
            print(f"Error adding API documentation: {str(e)}")
    
    print(f"External data integration complete. Added {docs_added} documents ({total_chunks} chunks).")
    return docs_added

if __name__ == "__main__":
    # When run as a script, load external data into the RAG engine
    from rag_engine import RAGEngine
    rag_engine = RAGEngine()
    docs_added = load_external_data(rag_engine)
    print(f"Added {docs_added} documents to the RAG engine.")
