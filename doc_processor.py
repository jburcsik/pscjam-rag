"""
Document processor module for handling text documents.
"""

class DocProcessor:
    """
    A simple document processor class that handles text preparation.
    """
    
    def __init__(self):
        """Initialize the DocProcessor."""
        pass
    
    def chunk_text(self, text, chunk_size=1000):
        """
        Split text into chunks of roughly equal size.
        
        Args:
            text (str): The text to split
            chunk_size (int): Maximum size of each chunk in characters
            
        Returns:
            list: List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        # Simple chunking by character count for now
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        
        return chunks
    
    def process_document(self, text):
        """
        Process a document for embedding.
        
        Args:
            text (str): Document text
            
        Returns:
            list: List of processed text chunks ready for embedding
        """
        # For now, just chunk the text
        chunks = self.chunk_text(text)
        return chunks
