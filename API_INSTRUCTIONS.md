# GC Forms RAG API

This is a Retrieval-Augmented Generation (RAG) system for GC Forms documentation. It provides accurate, context-specific answers about GC Forms and its API by using vector embeddings to find the most relevant content and generating helpful responses using OpenAI's GPT models.

## Live Demo

The API is hosted on Replit and can be accessed at:
https://pscjam-rag-1.jesseburcsik.repl.co/

## Features

- **Semantic Search**: Uses OpenAI embeddings (text-embedding-3-small model) for accurate, meaning-based search
- **AI-Generated Responses**: Provides natural language answers using OpenAI's GPT models
- **Data Sources**: Combines content from:
  - Canada.ca Forms website documentation
  - Forms API technical documentation
- **Persistent Cache**: Saves embeddings to reduce API costs and improve load times
- **Simple API**: Easy-to-use REST API for integration
- **Streaming Support**: Real-time response streaming via Server-Sent Events (SSE)
- **MCP Support**: Compatible with Model Context Protocol servers
- **Simplified Web Interface**: Clean, streamlined browser-based testing interface

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

Visit the URL above to use the streamlined web interface. Simply enter your question and:

- Click "Submit Query" for a standard response (AI-generated response followed by retrieved documents)
- Click "Stream Response" for a real-time streaming response using Server-Sent Events

The checkbox "Generate AI Response" is enabled by default to provide AI-generated answers using OpenAI's GPT models.

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
    "request_type": "user_query",
    "query": "How do I authenticate with the GC Forms API?"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))
data = response.json()
print(data)
```

### Option 1a: Streaming Responses with /api/mcp/stream

For real-time streaming responses using Server-Sent Events (SSE):

```python
import requests
import sseclient
import json

url = "https://pscjam-rag-1.jesseburcsik.repl.co/api/mcp/stream"
payload = {
    "request_type": "user_query",
    "query": "How do I authenticate with the GC Forms API?"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, json=payload, stream=True)
client = sseclient.SSEClient(response)

for event in client.events():
    if event.event == "document":
        # Process each retrieved document
        doc_data = json.loads(event.data)
        print(f"Document {doc_data['index']}: {doc_data['text'][:50]}...")
    elif event.event == "content":
        # Process each chunk of generated content
        content_data = json.loads(event.data)
        print(content_data["chunk"], end="")
    elif event.event == "end":
        # End of stream
        print("\nStream complete")
        break
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
