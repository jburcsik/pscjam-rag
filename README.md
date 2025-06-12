# Simple RAG System for MCP Server Support

A lightweight Retrieval-Augmented Generation (RAG) system designed to support an MCP server by providing information retrieval and code generation capabilities.

## Overview

This system uses OpenAI embeddings to create a simple but effective vector search over documentation, allowing it to:

1. Answer questions about documentation (inform)
2. Provide context for code generation (do code)
3. Support API calls through a web interface

## Features

- Simple document processing with text chunking
- Vector embeddings via OpenAI API
- In-memory vector storage with cosine similarity search
- Web UI for interactive queries
- API endpoints for MCP server integration
- Deployment ready for Replit

## Setup and Deployment

### Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python3 app.py
   ```

### Replit Deployment

1. Create a new Repl and import this repository
2. Add your OpenAI API key as a secret named `OPENAI_API_KEY`
3. The application should automatically install dependencies and start

## API Endpoints

### Query for Information
```
POST /api/inform
{
  "query": "What are the features of GC Forms?"
}
```

### Generate Code
```
POST /api/code
{
  "requirements": "Create a form with validation",
  "language": "javascript"
}
```

## Loading Additional Data

To add more documents to the knowledge base:

```python
from rag_engine import RAGEngine

engine = RAGEngine()
engine.add_document("Your document text here", {"type": "documentation", "source": "Source Name"})
```

## Next Steps

- Add persistent storage for embeddings
- Implement actual code generation using an LLM
- Add authentication for API endpoints
