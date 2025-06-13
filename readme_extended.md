# GC Forms RAG System: Extended Documentation

This document provides a comprehensive overview of the GC Forms Retrieval-Augmented Generation (RAG) system codebase. It explains each component's purpose, functionality, and how they work together to create a cohesive API-driven RAG system that can be integrated with Model Context Protocol (MCP) servers.

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Components](#core-components)
   - [Document Processing](#document-processing)
   - [Vector Storage](#vector-storage)
   - [RAG Engine](#rag-engine)
   - [MCP Support](#mcp-support)
   - [Streaming Support](#streaming-support)
3. [Data Sources](#data-sources)
   - [External Data Integration](#external-data-integration)
   - [Web Scraping](#web-scraping)
4. [API & Web Service](#api--web-service)
   - [API Endpoints](#api-endpoints)
   - [CORS Support](#cors-support)
   - [Web Interface](#web-interface)
5. [Embedding Persistence](#embedding-persistence)
   - [Cache Management](#cache-management)
6. [Deployment Options](#deployment-options)
   - [Local Development](#local-development)
   - [Replit Deployment](#replit-deployment)
   - [Docker Deployment](#docker-deployment)
7. [Integration Examples](#integration-examples)
   - [MCP Integration](#mcp-integration)
   - [Client Usage](#client-usage)
8. [Testing Scripts](#testing-scripts)
9. [File by File Documentation](#file-by-file-documentation)
10. [Configuration Files](#configuration-files)

## System Overview

The GC Forms RAG system is designed to provide accurate, context-specific answers about the GC Forms platform and its API by using vector embeddings to find relevant content and OpenAI's GPT models to generate helpful responses. The system combines document processing, vector storage, retrieval, and generative AI to create a powerful RAG application that can be consumed via API endpoints or through a simplified web interface.

Key features include:

- **Semantic Search**: Uses OpenAI's text-embedding-3-small model for accurate meaning-based search
- **AI-Generated Responses**: Provides natural language answers using OpenAI's GPT models
- **Multiple Data Sources**: Combines content from the Canada.ca Forms website and API documentation
- **Embedding Persistence**: Saves embeddings to JSON files to reduce API costs and improve load times
- **REST API**: Easy-to-use endpoints for integration with other applications
- **Streaming Support**: Provides real-time responses via Server-Sent Events (SSE)
- **MCP Support**: Compatible with Model Context Protocol servers for LLM integration
- **Simplified Web Interface**: Streamlined browser-based interface for testing the API
- **Multiple Deployment Options**: Support for local, Replit, and Docker deployments

## Core Components

### Document Processing

**File**: `doc_processor.py`

The Document Processor is responsible for preparing text documents for embedding. It handles the chunking of large documents into smaller, more manageable pieces that can be effectively embedded.

**Key Functions**:
- `chunk_text(text, chunk_size=1000)`: Splits text into chunks of roughly equal size
- `process_document(text)`: Processes a document for embedding by chunking it

The current implementation uses a simple character-based chunking strategy, dividing documents into 1000-character chunks. This approach ensures that documents aren't too large for the embedding model to handle effectively.

### Vector Storage

**File**: `vector_store.py`

The Vector Store manages the creation, storage, and retrieval of text embeddings. It uses OpenAI's API to generate embeddings for text chunks and implements a simple in-memory storage system with cosine similarity search.

**Key Functions**:
- `create_embedding(text)`: Creates an embedding vector for the given text using OpenAI API
- `add_document(text, metadata=None)`: Adds a document to the vector store
- `search(query, top_k=3)`: Searches for the most similar documents to a query
- `save_embeddings(file_path)`: Saves embeddings to a cache file
- `load_embeddings(file_path)`: Loads embeddings from a cache file

The Vector Store uses the text-embedding-3-small model from OpenAI, which provides high-quality embeddings while being efficient. Cosine similarity is used to compare query embeddings with document embeddings to find the most relevant content.

### RAG Engine

**File**: `rag_engine.py`

The RAG Engine combines the Document Processor and Vector Store to create a complete RAG system. It manages the processing of documents, storage of embeddings, and retrieval of relevant information for queries.

**Key Functions**:
- `add_document(text, metadata=None)`: Processes and adds a document to the vector store
- `query(query_text)`: Processes a query and returns relevant results

The RAG Engine acts as a coordinator between the Document Processor and Vector Store, ensuring that documents are properly processed before being added to the vector store and that queries are handled efficiently.

### MCP Support

**File**: `mcp_support.py`

The MCP Support Engine extends the basic RAG engine to support integration with Model Context Protocol (MCP) servers. It provides enhanced functionality for informational queries and code generation.

**Key Functions**:
- `process_mcp_request(data)`: Processes MCP requests based on request_type
- `_generate_response_from_context(query, results)`: Generates AI responses using OpenAI's GPT models
- `_call_openai_completion(prompt)`: Makes API calls to OpenAI's chat completion endpoint
- `_generate_rule_based_response(query, results)`: Provides a fallback if API calls fail

This component is designed to provide a bridge between the RAG system and MCP servers, making it easy to enhance LLMs with domain-specific knowledge about GC Forms.

### Streaming Support

**Files**: `streaming.py`, `app.py` (`mcp_stream_endpoint` function)

The streaming support provides real-time responses using Server-Sent Events (SSE), allowing for a more interactive user experience.

**Key Functions**:
- `sse_response(generator_func)`: Creates a streaming response for SSE
- `stream_response_generator(query, rag_engine, mcp_engine)`: Generates a stream of events
- Events include:
  - `start`: Indicates the stream has started
  - `thinking`: Updates on processing progress
  - `document`: Each retrieved document with its content
  - `sources`: Summary of found sources
  - `generating`: Indicates AI response generation has started
  - `content`: Chunks of the AI-generated response
  - `end`: Indicates the stream has completed

This mechanism allows for a responsive interface where users can see documents and AI-generated responses appear in real-time as they're processed.

## Data Sources

### External Data Integration

**File**: `external_data.py`

The External Data Integration module loads data from multiple sources into the RAG system. It handles the integration of content from the Canada.ca Forms website and the Forms API documentation.

**Key Functions**:
- `load_external_data(rag_engine, use_cache=True)`: Loads external data from both the Canada.ca Forms website and Forms API documentation

This module supports caching of external data to improve performance and reduce the need to repeatedly scrape websites.

### Web Scraping

**Files**: `web_scraper.py`, `api_doc_scraper.py`

These modules handle the collection of data from web sources. The Web Scraper extracts content from the Canada.ca Forms website, while the API Doc Scraper collects information from the Forms API documentation.

**Key Classes and Functions**:
- `WebScraper`: Scrapes content from the Canada.ca Forms website
- `scrape_canada_forms_website(max_pages=30)`: Function to scrape the website and return collected documents

## API & Web Service

### API Endpoints

**Files**: `app.py`

This file implements the web server and API endpoints for the RAG system with embedding caching capabilities. It provides both retrieval functionality and AI-generated responses.

**Key Endpoints**:
- `GET /`: Home page with streamlined API tester interface
- `GET /simple`: Alternative simple interface (backup)
- `POST /query`: POST-based query endpoint for retrieving relevant documents
- `POST /api/search`: Alternative search endpoint, functionally identical to `/query`
- `POST /api/mcp`: MCP endpoint for integration with LLM systems, returns AI-generated responses
- `POST /api/mcp/stream`: Streaming version of the MCP endpoint using Server-Sent Events (SSE)
- `GET /health`: Health check endpoint

The main endpoints have been streamlined to focus on core functionality:
1. Document retrieval (`/query` and `/api/search`)
2. AI-generated responses (`/api/mcp`)
3. Streaming responses (`/api/mcp/stream`)

### CORS Support

The API includes comprehensive CORS support to enable cross-origin requests, making it easy to integrate with web applications hosted on different domains.

**Implementation**:
```python
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response
```

### Web Interface

**File**: `static/index.html`

The web interface provides a simplified way to interact with the RAG system directly from a browser. It includes:

- A form for entering queries
- A "Submit Query" button for standard responses
- A "Stream Response" button for real-time streaming responses
- A checkbox to toggle AI-generated responses (enabled by default)
- Display sections for both AI-generated responses and retrieved documents
- Support for streaming results via Server-Sent Events

The UI is designed to place AI-generated responses at the top for better user experience, followed by the retrieved source documents below. The interface has been streamlined to focus on core functionality, removing unnecessary tabs and documentation panels.

## Embedding Persistence

**Files**: `vector_store.py`, `cache_embeddings.py`

Embedding persistence is a key feature that saves embeddings to a JSON file to reduce API costs and improve load times. This is implemented through the save_embeddings and load_embeddings methods in the VectorStore class.

**Key Functions**:
- `save_embeddings(file_path="embeddings_cache.json")`: Saves embeddings to a cache file
- `load_embeddings(file_path="embeddings_cache.json")`: Loads embeddings from a cache file

### Cache Management

**File**: `manage_cache.py`

This utility script provides functions for managing the embedding cache.

**Key Functions**:
- `create_cache()`: Creates a fresh embeddings cache by processing all available data
- `inspect_cache(cache_file="embeddings_cache.json")`: Inspects the contents of the cache file
- `delete_cache(cache_file="embeddings_cache.json")`: Deletes the cache file

## Deployment Options

### Local Development

The system can be easily run locally for development purposes with the following steps:

1. Create a `.env` file with OpenAI API key
2. Install dependencies with `pip install -r requirements.txt`
3. Run the application with `python app.py`

### Replit Deployment

**Files**: `.replit`, `replit_setup.sh`, `start.sh`

The system includes configuration files for deploying to Replit, making it easy to host the RAG API without managing infrastructure.

**Key Files**:
- `.replit`: Configuration for Replit environment
- `replit_setup.sh`: Setup script for Replit deployment
- `start.sh`: Script to start the application on Replit

### Docker Deployment

**File**: `Dockerfile`

The system also includes a Docker configuration for containerized deployment.

```Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
```

## Integration Examples

### MCP Integration

**Files**: `mcp_integration_example.py`, `mcp_connector.py`

These files provide examples of how to integrate the RAG API with an MCP server.

**Key Components**:
- `MCPServerIntegration`: Class that simulates an MCP server integrating with the RAG API
- `GCFormsRagConnector`: Connector for enriching LLM prompts with GC Forms documentation from the RAG API

### Client Usage

**File**: `client_example.py`

This file demonstrates how to use the RAG API from a client application.

**Key Functions**:
- `query_rag_api(question)`: Sends a query to the RAG API and returns the results
- `display_results(data)`: Displays the results from the RAG API in a readable format

## Testing Scripts

**Files**: `test_api_key.py`, `test_env.py`, `test_external_data.py`

These scripts provide ways to test different aspects of the system.

**Key Files**:
- `test_api_key.py`: Tests that the API key is being loaded correctly
- `test_env.py`: Tests environment variable configuration
- `test_external_data.py`: Tests the loading of external data

## File by File Documentation

### Core Files

- **api_secrets.py**: Manages API keys and endpoints securely
- **app.py**: Main web server with API endpoints and embedding caching
- **cache_embeddings.py**: Utilities for saving and loading embeddings
- **data_loader.py**: Functions for loading comprehensive data into the RAG system
- **doc_processor.py**: Handles document preparation and chunking
- **external_data.py**: Integrates external data from multiple sources
- **main.py**: Basic demonstration script for the RAG system
- **main_with_cache.py**: Enhanced demonstration with embedding caching
- **manage_cache.py**: Script to manage the embedding cache
- **mcp_connector.py**: Client for connecting an MCP server to the RAG API
- **mcp_integration_example.py**: Example of MCP server integration
- **mcp_support.py**: Enhanced RAG engine for MCP support and AI response generation
- **rag_engine.py**: Core RAG functionality
- **streaming.py**: Server-Sent Events (SSE) for real-time streaming responses
- **sse_utils.py**: Utilities for server-sent events
- **vector_store.py**: Embedding storage and retrieval
- **web_scraper.py**: Scraper for the Canada.ca forms website

### Data Files

- **canada_forms_content.json**: Scraped content from the Canada.ca Forms website
- **api_docs_content.json**: API documentation content
- **embeddings_cache.json**: Cache file for embeddings

### Web Interface Files

- **static/index.html**: Streamlined web interface for testing the API
- **static/simple_index.html**: Backup version of the web interface

### Deployment Files

- **.replit**: Replit configuration
- **replit_setup.sh**: Setup script for Replit
- **replit.nix**: Nix environment for Replit
- **Dockerfile**: Container configuration
- **vercel.json**: Vercel deployment configuration
- **start.sh**: Startup script for deployments

### Documentation Files

- **API_INSTRUCTIONS.md**: Instructions for API users
- **README.md**: Basic project readme

### Testing Files

- **test_api_key.py**: Tests API key loading
- **test_env.py**: Tests environment variables
- **test_external_data.py**: Tests external data loading

## Configuration Files

### requirements.txt

Lists all Python dependencies required by the project:

```
flask
requests
python-dotenv
beautifulsoup4
```

### .env.example

Template for creating a .env file with required environment variables:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1/embeddings
```

## Data Flow

The system follows this typical data flow:

1. **Initialization**:
   - Load API keys from environment or secrets
   - Check for cached embeddings
   - If no cache, load external data from sources
   - Process and embed documents
   - Save embeddings to cache

2. **Standard Query Processing**:
   - Receive query via `/query` or `/api/search` endpoint
   - Create embedding for the query
   - Compare query embedding to document embeddings using cosine similarity
   - Return most relevant document chunks

3. **MCP Query Processing**:
   - Receive query via `/api/mcp` endpoint
   - Create embedding for the query
   - Find most relevant document chunks via cosine similarity
   - Format a prompt with the retrieved context
   - Send prompt to OpenAI's GPT model
   - Return both AI-generated response and relevant document chunks

4. **Streaming Response Processing**:
   - Receive query via `/api/mcp/stream` endpoint
   - Set up Server-Sent Events (SSE) connection
   - Stream document chunks as they are retrieved
   - Stream AI-generated response in chunks as it's being generated
   - Send event types to indicate progress (start, thinking, document, generating, content, end)

5. **Web Interface Flow**:
   - User submits query via form
   - If "Generate AI Response" is checked (default), call `/api/mcp` endpoint
   - Display AI response at the top of the page
   - Call `/query` endpoint to retrieve and display relevant documents
   - Or use "Stream Response" button for real-time updates via SSE

## Conclusion

The GC Forms RAG system provides a powerful way to access and query information about the GC Forms platform and its API. Its modular architecture makes it easy to extend and integrate with other systems, while its embedding persistence capabilities ensure efficient operation.

The system leverages OpenAI's GPT models to generate helpful AI responses based on retrieved documents, providing users with natural language answers to their questions. The streamlined web interface puts AI-generated responses front and center while still giving access to the source documents for reference.

Real-time streaming capabilities via Server-Sent Events create a more dynamic and engaging experience, allowing users to see both search results and AI responses as they're being generated.

The system is designed to be deployed in various environments (local, Replit, Docker) and offers multiple integration options, including direct API endpoints and MCP server enrichment. The comprehensive documentation and examples make it easy for developers to understand and use the system effectively.
