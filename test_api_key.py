"""
Simple test to verify that the API key is being loaded correctly.
"""
from api_secrets import get_api_key, get_api_endpoint

print("Testing API key loading...")
api_key = get_api_key()
if api_key:
    # Show just the first few characters to verify it's loaded
    print(f"API key loaded successfully: {api_key[:10]}...")
else:
    print("Failed to load API key!")

print(f"API endpoint: {get_api_endpoint()}")
