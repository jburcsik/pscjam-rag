"""
Test OpenAI API credentials.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Testing environment variables:")
print(f"OPENAI_API_KEY exists: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"OPENAI_ENDPOINT exists: {'Yes' if os.getenv('OPENAI_ENDPOINT') else 'No'}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:10]}... (first 10 characters)")
print(f"OPENAI_ENDPOINT: {os.getenv('OPENAI_ENDPOINT')}")
