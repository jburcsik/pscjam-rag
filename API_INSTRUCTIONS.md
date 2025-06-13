# GC Forms RAG API

This is a Retrieval-Augmented Generation (RAG) system for GC Forms documentation. It provides accurate, context-specific answers about GC Forms and its API by using vector embeddings to find the most relevant content.

## Live Demo

The API is hosted on Replit and can be accessed at:
https://pscjam-rag-1.jesseburcsik.repl.co/

## Features

- **Semantic Search**: Uses OpenAI embeddings for accurate, meaning-based search
- **Data Sources**: Combines content from:
  - Canada.ca Forms website documentation
  - Forms API technical documentation
- **Persistent Cache**: Saves embeddings to reduce API costs and improve load times
- **Simple API**: Easy-to-use REST API for integration
- **MCP Support**: Compatible with Model Context Protocol servers
- **Web Interface**: Browser-based testing interface included

## Setup and Deployment

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fresh-rag
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_API_BASE=https://api.openai.com/v1/embeddings
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. The server will run at http://localhost:8080

### Replit Deployment

1. Create a new Replit and import the repository
2. Add your OpenAI API key as a Secret named `OPENAI_API_KEY`
3. The system will automatically deploy and run

### Docker Deployment

```
docker build -t gcforms-rag .
docker run -p 8080:8080 -e OPENAI_API_KEY=your_api_key_here gcforms-rag
```

## How to Use the API

### Option 1: Web Interface

Visit the URL above to use the web interface. Simply enter your question and click "Submit Query".

### Option 2: API Endpoint

Send a POST request to the `/query` endpoint:

```python
import requests
import json

url = "https://pscjam-rag-1.jesseburcsik.repl.co/query"
payload = {"query": "How do I authenticate with the GC Forms API?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))
data = response.json()
print(data["results"])
```

### Example Response

```json
{
  "query": "How do I authenticate with the GC Forms API?",
  "results": [
    {
      "text": "Authentication: Most endpoints require an API key...",
      "metadata": {
        "source": "API Documentation",
        "section": "Authentication"
      },
      "similarity": 0.89
    },
    ...
  ]
}
```

## Integration with MCP Server

### Option 1: Direct /api/mcp Endpoint

You can directly call our `/api/mcp` endpoint which handles the retrieval and combines it with MCP:

```python
import requests
import json

url = "https://pscjam-rag-1.jesseburcsik.repl.co/api/mcp"
payload = {
    "messages": [
        {"role": "user", "content": "How do I authenticate with the GC Forms API?"}
    ]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))
data = response.json()
print(data)
```

### Option 2: Enrich Your MCP Server

For a more flexible approach, you can enrich your existing MCP server with RAG context:

1. First, query our `/query` endpoint to get relevant information
2. Then insert a system message with this context into your MCP request
3. Send the enriched request to your LLM provider

We've provided a complete example in `mcp_integration_example.py` that shows how to:

- Extract the user's question from MCP messages
- Query our RAG API to get relevant context
- Insert context as a system message
- Create an enriched MCP request

This approach gives you more control over how the RAG context is used.

## Use Cases

1. **Answering Questions**: Get accurate answers about GC Forms functionality and API usage.
2. **Code Examples**: Request examples of how to use specific API features.
3. **Documentation Lookup**: Find specific information from the GC Forms documentation.

## Features

- **Semantic Search**: Uses vector embeddings to find the most semantically relevant content
- **Persistant Cache**: Saves embeddings to avoid recreating them on each run
- **Multiple Data Sources**: Integrates content from Canada.ca Forms website and API documentation
- **MCP Support**: Compatible with Model Context Protocol for LLM integration

## Contact

For any questions or assistance with integrating the API, please reach out.
