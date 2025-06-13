"""
Web server for the RAG system with MCP support.
"""
from flask import Flask, request, jsonify, send_from_directory, make_response
import os
from rag_engine import RAGEngine
from mcp_support import MCPSupportEngine

app = Flask(__name__)
rag_engine = RAGEngine()
mcp_engine = MCPSupportEngine()

# Enable CORS for all routes without using flask-cors
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Handle OPTIONS requests for CORS preflight
@app.route('/', methods=['OPTIONS'])
@app.route('/query', methods=['OPTIONS'])
@app.route('/api/mcp', methods=['OPTIONS'])
@app.route('/api/search', methods=['OPTIONS'])
@app.route('/api/code', methods=['OPTIONS'])
def handle_options():
    return make_response('', 204)

# Initialize with comprehensive data
def initialize_data():
    """Initialize the RAG engine with comprehensive GC Forms data."""
    try:
        # Use our data loader to add comprehensive documentation
        from data_loader import load_gc_forms_data
        docs_added = load_gc_forms_data(rag_engine)
        
        # Also initialize the MCP engine with the same data
        load_gc_forms_data(mcp_engine)
        
        print(f"Initialization complete! Added {docs_added} documents to the knowledge base.")
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
    """Home page with API tester."""
    # Check if static directory exists, if not create it
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Check if index.html exists
    index_path = os.path.join(static_dir, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory('static', 'index.html')
    else:
        # Fallback if the file doesn't exist
        return """
        <html>
            <head><title>GC Forms RAG API</title></head>
            <body>
                <h1>GC Forms RAG API</h1>
                <p>Use the /query endpoint to access the RAG system.</p>
                <p>POST to /query with JSON: {"query": "your question here"}</p>
            </body>
        </html>
        """

@app.route('/query')
def query():
    """Query the RAG engine."""
    query_text = request.args.get('q', '')
    if not query_text:
        return jsonify({"error": "No query provided", "results": []})
    
    results = rag_engine.query(query_text)
    return jsonify({"results": results})

@app.route('/api/inform', methods=['POST'])
def inform_user():
    """API endpoint for informational queries."""
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    response = mcp_engine.inform_user(data['query'])
    return jsonify(response)

@app.route('/api/mcp', methods=['POST'])
def mcp_endpoint():
    """MCP endpoint for integration with LLM systems."""
    try:
        data = request.get_json()
        response = mcp_engine.process_mcp_request(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def query_endpoint():
    """Simple query endpoint for external consumers."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
            
        query_text = data['query']
        results = rag_engine.query(query_text)
        
        return jsonify({
            "query": query_text,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/code', methods=['POST'])
def generate_code():
    """API endpoint for code generation."""
    data = request.json
    if not data or 'requirements' not in data:
        return jsonify({"error": "No requirements provided"}), 400
    
    language = data.get('language', 'python')
    response = mcp_engine.generate_code(data['requirements'], language)
    return jsonify(response)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from the 'static' directory."""
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "embeddings_count": len(rag_engine.vector_store.embeddings),
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })

# Initialize data at startup
initialize_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
