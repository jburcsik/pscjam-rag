"""
Web server for the RAG system with MCP support.
"""
from flask import Flask, request, jsonify
from rag_engine import RAGEngine
from mcp_support import MCPSupportEngine

app = Flask(__name__)
rag_engine = RAGEngine()
mcp_engine = MCPSupportEngine()

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
    """Home page."""
    return """
    <html>
        <head>
            <title>GC Forms RAG System</title>
            <style>
                body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; line-height: 1.6; color: #333; background: #f7f9fc; }
                .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
                header { background: #4285f4; color: white; padding: 20px 0; margin-bottom: 30px; }
                header .container { display: flex; justify-content: space-between; align-items: center; }
                header h1 { margin: 0; font-size: 24px; font-weight: 500; }
                .search-box { background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 30px; }
                .tabs { display: flex; margin-bottom: 20px; border-bottom: 1px solid #ddd; }
                .tab { padding: 10px 20px; cursor: pointer; border-bottom: 2px solid transparent; }
                .tab.active { border-bottom: 2px solid #4285f4; color: #4285f4; font-weight: 500; }
                form { margin: 20px 0; }
                input[type="text"] { width: 75%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
                button { padding: 12px 20px; background: #4285f4; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; transition: background 0.2s; }
                button:hover { background: #3b78e7; }
                #results { margin-top: 20px; }
                .result-item { background: white; margin-bottom: 20px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
                .result-item h3 { margin-top: 0; color: #4285f4; }
                .similarity-badge { display: inline-block; background: #e8f0fe; color: #4285f4; padding: 3px 8px; border-radius: 12px; font-size: 14px; }
                .metadata { font-size: 14px; color: #666; margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; }
                pre { background: #f1f3f4; padding: 15px; border-radius: 4px; overflow-x: auto; }
                .api-section { background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 30px; }
                .hidden { display: none; }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>GC Forms RAG System</h1>
                    <span>Retrieval-Augmented Generation for GC Forms Documentation</span>
                </div>
            </header>
            
            <div class="container">
                <div class="tabs">
                    <div class="tab active" data-tab="search">Search</div>
                    <div class="tab" data-tab="api">API Documentation</div>
                    <div class="tab" data-tab="about">About</div>
                </div>
                
                <div id="search-content" class="tab-content">
                    <div class="search-box">
                        <h2>Search GC Forms Documentation</h2>
                        <p>Enter your question about GC Forms to search our knowledge base:</p>
                        <form id="queryForm">
                            <input type="text" id="query" placeholder="E.g., What security features does GC Forms have?">
                            <button type="submit">Search</button>
                        </form>
                    </div>
                    <div id="results"></div>
                </div>
                
                <div id="api-content" class="tab-content hidden">
                    <div class="api-section">
                        <h2>API Endpoints</h2>
                        <p>This RAG system provides the following API endpoints for integration with MCP servers:</p>
                        
                        <div class="result-item">
                            <h3>1. Basic Search API</h3>
                            <p>Retrieve relevant documents based on a query.</p>
                            <pre>GET /query?q=your+search+query</pre>
                            <div class="metadata">
                                Returns JSON with matching documents and similarity scores.
                            </div>
                        </div>
                        
                        <div class="result-item">
                            <h3>2. Inform User API</h3>
                            <p>Get information to answer user questions.</p>
                            <pre>POST /api/inform
Content-Type: application/json

{
  "query": "What security features does GC Forms have?"
}</pre>
                            <div class="metadata">
                                Returns JSON with information response and context.
                            </div>
                        </div>
                        
                        <div class="result-item">
                            <h3>3. Code Generation API</h3>
                            <p>Generate code examples based on documentation.</p>
                            <pre>POST /api/code
Content-Type: application/json

{
  "requirements": "Create a form with file upload",
  "language": "javascript"
}</pre>
                            <div class="metadata">
                                Returns JSON with generated code and context from documentation.
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="about-content" class="tab-content hidden">
                    <div class="api-section">
                        <h2>About This RAG System</h2>
                        <p>This is a simple Retrieval-Augmented Generation (RAG) system designed to support an MCP server by providing:</p>
                        <ul>
                            <li>Semantic search over GC Forms documentation</li>
                            <li>Context retrieval for question answering</li>
                            <li>Documentation-based code generation support</li>
                        </ul>
                        <p>The system uses vector embeddings from OpenAI to find the most relevant documentation for any query.</p>
                    </div>
                </div>
            </div>
            
            <script>
                // Tab navigation
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.addEventListener('click', () => {
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                        tab.classList.add('active');
                        
                        const tabName = tab.getAttribute('data-tab');
                        document.querySelectorAll('.tab-content').forEach(content => {
                            content.classList.add('hidden');
                        });
                        document.getElementById(tabName + '-content').classList.remove('hidden');
                    });
                });
                
                // Search form submission
                document.getElementById('queryForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const query = document.getElementById('query').value;
                    const resultsDiv = document.getElementById('results');
                    
                    resultsDiv.innerHTML = '<p>Searching...</p>';
                    
                    try {
                        const response = await fetch('/query?q=' + encodeURIComponent(query));
                        const data = await response.json();
                        
                        let html = '<h2>Results:</h2>';
                        if (data.results.length === 0) {
                            html += '<p>No results found.</p>';
                        } else {
                            data.results.forEach((result, i) => {
                                html += `
                                    <div class="result-item">
                                        <h3>${result.metadata.title || 'Result ' + (i+1)}</h3>
                                        <span class="similarity-badge">Similarity: ${result.similarity.toFixed(4)}</span>
                                        <p style="white-space: pre-line;">${result.text}</p>
                                        <div class="metadata">
                                            <p><strong>Section:</strong> ${result.metadata.section || 'general'}</p>
                                            <p><strong>Type:</strong> ${result.metadata.type || 'document'}</p>
                                        </div>
                                    </div>
                                `;
                            });
                        }
                        
                        resultsDiv.innerHTML = html;
                    } catch (error) {
                        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
                    }
                });
            </script>
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

@app.route('/api/code', methods=['POST'])
def generate_code():
    """API endpoint for code generation."""
    data = request.json
    if not data or 'requirements' not in data:
        return jsonify({"error": "No requirements provided"}), 400
    
    language = data.get('language', 'python')
    response = mcp_engine.generate_code(data['requirements'], language)
    return jsonify(response)

# Initialize data at startup
initialize_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
