# Simple RAG System for MCP Server Support

A lightweight Retrieval-Augmented Generation (RAG) system designed to support an MCP server by providing information retrieval and code generation capabilities.

## Overview

This system uses OpenAI embeddings to create a simple but effective vector search over documentation, allowing it to:

1. Answer questions about documentation
2. Provide context for code generation
3. Support API calls through a simple web interface
4. Generate AI responses using OpenAI's GPT models

## Features

- Simple document processing with text chunking
- Vector embeddings via OpenAI API (text-embedding-3-small model)
- In-memory vector storage with cosine similarity search
- Streamlined web UI for interactive queries
- API endpoints for MCP server integration
- Deployment ready for Replit
- Server-Sent Events (SSE) for streaming responses in real-time
- AI-generated responses using OpenAI's GPT models
- Embedding cache to avoid regenerating embeddings

## Setup and Deployment

### Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```
   python3 app.py
   ```

### Replit Deployment

1. Create a new Repl and import this repository
2. Add your OpenAI API key as a secret named `OPENAI_API_KEY`
3. The application should automatically install dependencies and start

## API Endpoints

### Basic Document Retrieval
```
POST /query
{
  "query": "What are the features of GC Forms?"
}
```
Returns relevant document chunks without AI-generated responses.

### Search Endpoint (Alternative to Query)
```
POST /api/search
{
  "query": "What are the features of GC Forms?"
}
```
Functionally identical to the `/query` endpoint.

### MCP Query
```
POST /api/mcp
{
  "request_type": "user_query",
  "query": "What are the features of GC Forms?"
}
```
This endpoint returns AI-generated responses using OpenAI's GPT models based on retrieved documents.

### Streaming Responses with SSE
```
POST /api/mcp/stream
{
  "request_type": "user_query",
  "query": "What are the features of GC Forms?"
}
```
This endpoint returns a stream of Server-Sent Events (SSE) for real-time updates as the system:
1. Searches for relevant documents
2. Returns document matches incrementally
3. Generates the AI response sentence by sentence using OpenAI's completions API

The frontend can process these events to create a more dynamic and engaging user experience.

## Loading Additional Data

To add more documents to the knowledge base:

```python
from rag_engine import RAGEngine

engine = RAGEngine()
engine.add_document("Your document text here", {"type": "documentation", "source": "Source Name"})
```

## Testing

Run the test scripts to verify that everything is working correctly:

```bash
# Test the OpenAI completions integration
python test_openai.py

# Test the local API endpoints
python test_local.py

# Test the streaming SSE endpoint
python test_sse.py

# Test the Replit deployment (if applicable)
python test_replit.py
```

## Next Steps

- Improve prompt engineering for better responses
- Add persistent storage for embeddings
- Enhance error handling and fallback mechanisms
- Add authentication for API endpoints
- Support multiple document collections
