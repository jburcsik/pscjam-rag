"""
RAG Engine module that combines document processing, vector storage, and generation.
"""
from doc_processor import DocProcessor
from vector_store import VectorStore

class RAGEngine:
    """
    A simple Retrieval-Augmented Generation engine.
    """
    
    def __init__(self):
        """Initialize the RAG Engine with document processor and vector store."""
        self.doc_processor = DocProcessor()
        self.vector_store = VectorStore()
    
    def add_document(self, text, metadata=None):
        """
        Process and add a document to the vector store.
        
        Args:
            text (str): Document text
            metadata (dict, optional): Metadata about the document
            
        Returns:
            int: Number of chunks added successfully
        """
        chunks = self.doc_processor.process_document(text)
        print(f"Processed document into {len(chunks)} chunks")
        
        success_count = 0
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata["chunk_id"] = i
            result = self.vector_store.add_document(chunk, chunk_metadata)
            if result:
                success_count += 1
            else:
                print(f"Failed to add chunk {i}")
        
        print(f"Successfully added {success_count}/{len(chunks)} chunks")
        return success_count
    
    def query(self, query_text):
        """
        Process a query and return results.
        
        Args:
            query_text (str): The query text
            
        Returns:
            list: List of relevant document chunks
        """
        results = self.vector_store.search(query_text)
        return results
