#!/bin/bash
# Simple script to test local endpoints of the RAG system

echo "Testing local RAG endpoints..."
echo "------------------------------"

# Test the query endpoint
echo "1. Testing /query endpoint:"
echo "Query: What is GC Forms?"
echo ""
curl -X POST http://localhost:5001/query \
     -H "Content-Type: application/json" \
     -d '{"query":"What is GC Forms?"}' | python3 -m json.tool

echo ""
echo "------------------------------"
echo "2. Testing /api/mcp endpoint:"
echo "Query: What is GC Forms?"
echo ""
curl -X POST http://localhost:5001/api/mcp \
     -H "Content-Type: application/json" \
     -d '{"request_type":"user_query","query":"What is GC Forms?"}' | python3 -m json.tool

echo ""
echo "------------------------------"
echo "If you don't see proper responses, make sure your local server is running on port 5001."
echo "Run: python app.py"
