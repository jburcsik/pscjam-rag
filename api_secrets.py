"""
Secrets management for Replit deployment.
This will allow us to use environment variables from Replit Secrets.
"""
import os
from os import environ

# Load .env file at import time
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded .env file")
except ImportError:
    print("dotenv package not found, .env file not loaded")

def get_api_key():
    """Get OpenAI API key from environment variables."""
    # Try to get from different possible sources
    # 1. From environment variables (includes those loaded from .env)
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    # 2. For Replit, get from Replit Secrets
    if 'REPL_ID' in os.environ:
        return os.environ.get('OPENAI_API_KEY')
    
    # If we get here, we don't have a key
    print("WARNING: No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")
    return None

def get_api_endpoint():
    """Get OpenAI API endpoint from environment variables."""
    # For Replit, get from Replit Secrets
    if 'REPL_ID' in os.environ:
        return os.environ.get('OPENAI_ENDPOINT', "https://api.openai.com/v1/embeddings")
    
    # For local development, use the default endpoint
    return "https://api.openai.com/v1/embeddings"
