"""
Vector Store module for embedding storage and retrieval.
"""
import requests
import json
import math
import os
from api_secrets import get_api_key, get_api_endpoint

class VectorStore:
    """
    A simple vector store for embeddings using OpenAI.
    """
    
    def __init__(self, api_key=None, endpoint=None):
        """Initialize the VectorStore with API credentials."""
        # Get credentials from secrets or use provided ones
        self.api_key = api_key or get_api_key()
        self.endpoint = endpoint or get_api_endpoint()
        self.embeddings = []  # Store our embeddings with metadata in memory
    
    def create_embedding(self, text):
        """
        Create an embedding vector for the given text using OpenAI API.
        
        Args:
            text (str): The text to create an embedding for
            
        Returns:
            list: The embedding vector
        """
        try:
            print(f"Sending request to OpenAI for text: {text[:50]}...")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # Using the latest embedding model from OpenAI
            data = {
                "input": text,
                "model": "text-embedding-3-small"  # Newer, more efficient model
            }
            
            print(f"Calling OpenAI API at: {self.endpoint}")
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 200:
                print("Successfully received embedding")
                embedding = response.json()["data"][0]["embedding"]
                print(f"Embedding length: {len(embedding)}")
                return embedding
            else:
                print(f"API Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return None
    
    def add_document(self, text, metadata=None):
        """
        Add a document to the vector store.
        
        Args:
            text (str): The document text
            metadata (dict, optional): Metadata about the document
        """
        embedding = self.create_embedding(text)
        if embedding:
            self.embeddings.append({
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {}
            })
            return True
        return False
    
    def search(self, query, top_k=3):
        """
        Search for most similar documents to the query.
        This is a very simple implementation using cosine similarity.
        
        Args:
            query (str): Query text
            top_k (int): Number of results to return
            
        Returns:
            list: List of documents sorted by similarity
        """
        # If no embeddings, return empty list
        if not self.embeddings:
            return []
            
        # Get embedding for query
        query_embedding = self.create_embedding(query)
        if not query_embedding:
            return []
            
        # Calculate cosine similarity with each document
        results = []
        for doc in self.embeddings:
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
                
            results.append({
                "text": doc["text"],
                "metadata": doc["metadata"],
                "similarity": similarity
            })
            
        # Sort by similarity (highest to lowest)
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top_k results
        return results[:top_k]
        
    def _cosine_similarity(self, vec1, vec2):
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1 (list): First vector
            vec2 (list): Second vector
            
        Returns:
            float: Cosine similarity score
        """
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        # Return cosine similarity
        return dot_product / (magnitude1 * magnitude2)
    
    def save_embeddings(self, file_path="embeddings_cache.json"):
        """
        Save embeddings to a cache file.
        
        Args:
            file_path: Path to save the embeddings cache
        
        Returns:
            bool: True if embeddings were successfully saved
        """
        try:
            print(f"Saving {len(self.embeddings)} embeddings to {file_path}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.embeddings, f)
            
            print(f"Successfully saved embeddings cache.")
            return True
        except Exception as e:
            print(f"Error saving embeddings: {str(e)}")
            return False
    
    def load_embeddings(self, file_path="embeddings_cache.json"):
        """
        Load embeddings from a cache file.
        
        Args:
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
                self.embeddings = json.load(f)
            
            print(f"Successfully loaded {len(self.embeddings)} embeddings.")
            return True
        except Exception as e:
            print(f"Error loading embeddings: {str(e)}")
            return False
