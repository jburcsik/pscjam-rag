#!/bin/bash
# Simple test script for the MCP endpoint
echo "Testing MCP endpoint..."
curl -X POST http://localhost:5001/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"request_type":"user_query","query":"is this tool useful?"}' \
  | jq .

echo -e "\n\nTesting regular query endpoint..."
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query":"is this tool useful?"}' \
  | jq .
