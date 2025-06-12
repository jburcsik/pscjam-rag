"""
Secrets management for Replit deployment.
This will allow us to use environment variables from Replit Secrets.
"""
import os
from os import environ

def get_api_key():
    """Get OpenAI API key from environment variables."""
    # Try to get from different possible sources
    # 1. For Replit, get from Replit Secrets
    if 'REPL_ID' in os.environ:
        return os.environ.get('OPENAI_API_KEY')
    # 2. From environment variables
    elif os.environ.get('OPENAI_API_KEY'):
        return os.environ.get('OPENAI_API_KEY')
    # 3. From .env file if exists (requires python-dotenv)
    else:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            return os.environ.get('OPENAI_API_KEY')
        except ImportError:
            pass
    
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
