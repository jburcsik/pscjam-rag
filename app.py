"""
Web server for the RAG system with MCP support and embedding caching.
"""
from flask import Flask, request, jsonify, send_from_directory
import os
from rag_engine import RAGEngine
from mcp_support import MCPSupportEngine
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)
# Initialize RAG engine first
rag_engine = RAGEngine()
# Create MCP engine with shared vector store
mcp_engine = MCPSupportEngine(shared_rag_engine=rag_engine)

# Initialize with comprehensive data and use embedding cache
def initialize_data():
    """Initialize the RAG engine with comprehensive GC Forms data using cache when available."""
    try:
        # Check for cached embeddings
        embeddings_cache = "embeddings_cache.json"
        cache_loaded = False
        
        # Try to load cached embeddings for RAG engine
        if os.path.exists(embeddings_cache):
            print(f"Found embeddings cache at {embeddings_cache}")
            cache_loaded = rag_engine.vector_store.load_embeddings(embeddings_cache)
            print(f"Loaded {len(rag_engine.vector_store.embeddings)} embeddings from cache")
        
        if not cache_loaded:
            print("No cache found or failed to load. Creating new embeddings...")
            # Use our data loader to add comprehensive documentation
            from data_loader import load_gc_forms_data
            docs_added = load_gc_forms_data(rag_engine)
            
            # Save embeddings for future use
            print("Saving embeddings to cache...")
            rag_engine.vector_store.save_embeddings(embeddings_cache)
            
            print(f"Initialization complete! Added {docs_added} documents to the knowledge base.")
        else:
            print("Successfully initialized RAG engine from cache")
        
        # Since MCP engine now shares the RAG engine's vector store,
        # we don't need to load or save separate embeddings for it
        print("MCP engine is using the same vector store as RAG engine - no need to reload embeddings")
    except Exception as e:
        print(f"Error during initialization: {e}")
        print("Falling back to basic demo data...")
        
        # Sample 1: GC Forms Overview (fallback)
        gc_forms_overview = """
        GC Forms is a powerful form creation and management system.
        It allows users to create custom forms for data collection,
        surveys, and feedback. Forms can be shared with specific users
        or made public. Results are automatically collected and can be
        exported in various formats.
        """
        
        rag_engine.add_document(gc_forms_overview, {"type": "overview", "source": "GC Forms Documentation"})
        mcp_engine.add_document(gc_forms_overview, {"type": "overview", "source": "GC Forms Documentation"})
        
        # Sample 2: GC Forms Features (fallback)
        gc_forms_features = """
        Key features of GC Forms include:
        1. Drag-and-drop form builder
        2. Multiple question types (text, multiple choice, checkboxes)
        3. Conditional logic for dynamic forms
        4. File upload capabilities
        5. Automatic data validation
        6. Real-time collaboration
        7. Response analytics and visualization
        8. Integration with other systems via APIs
        """
        
        rag_engine.add_document(gc_forms_features, {"type": "features", "source": "GC Forms Documentation"})
        mcp_engine.add_document(gc_forms_features, {"type": "features", "source": "GC Forms Documentation"})
        
        print("Basic initialization complete with fallback data.")

@app.route('/')
def home():
    """Home page that serves the demo interface."""
    return send_from_directory('static', 'index.html')
    
@app.route('/simple')
def simple():
    """The simple version of the demo interface (for backup)."""
    return send_from_directory('static', 'simple_index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

@app.route('/query', methods=['POST'])
def query_endpoint():
    """Simple query endpoint for external consumers."""
    try:
        print(f"Query endpoint called with method: {request.method}")
        print(f"Request data: {request.data}")
        data = request.get_json()
        print(f"Parsed JSON data: {data}")
        
        if not data or 'query' not in data:
            print("Error: No query provided in request")
            return jsonify({"error": "No query provided"}), 400
            
        query_text = data['query']
        print(f"Processing query: {query_text}")
        results = rag_engine.query(query_text)
        print(f"Found {len(results)} results")
        
        return jsonify({
            "query": query_text,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    """Search endpoint."""
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    results = rag_engine.query(query)
    
    return jsonify({
        "query": query,
        "results": results
    })

@app.route('/api/mcp', methods=['POST'])
def mcp_endpoint():
    """MCP endpoint for integration with LLM systems."""
    try:
        print(f"MCP endpoint called with method: {request.method}")
        print(f"MCP request data: {request.data}")
        data = request.get_json()
        print(f"MCP parsed JSON data: {data}")
        
        if not data or 'request_type' not in data:
            print("Error: Invalid MCP request format")
            return jsonify({"error": "Invalid request format"}), 400
            
        print(f"Processing MCP request type: {data.get('request_type')}")
        response = mcp_engine.process_mcp_request(data)
        print(f"MCP response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in MCP endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mcp/stream', methods=['POST'])
def mcp_stream_endpoint():
    """MCP endpoint that streams responses using Server-Sent Events (SSE)."""
    try:
        from streaming import sse_response, stream_response_generator
        
        print(f"SSE MCP endpoint called with method: {request.method}")
        print(f"SSE MCP request data: {request.data}")
        data = request.get_json()
        print(f"SSE MCP parsed JSON data: {data}")
        
        if not data or 'request_type' not in data:
            print("Error: Invalid MCP request format")
            return jsonify({"error": "Invalid request format"}), 400
            
        query = data.get('query', '')
        request_type = data.get('request_type')
        
        print(f"Processing streaming request for query: {query}")
        
        # Return a streaming response using the generator
        return sse_response(lambda: stream_response_generator(query, rag_engine, mcp_engine))
        
    except Exception as e:
        print(f"Error in SSE MCP endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "embeddings_count": len(rag_engine.vector_store.embeddings)
    })

if __name__ == '__main__':
    print("Initializing RAG system with caching...")
    initialize_data()
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5001)
