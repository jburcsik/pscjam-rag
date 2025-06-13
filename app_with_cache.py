"""
Web server for the RAG system with MCP support and embedding caching.
"""
from flask import Flask, request, jsonify
from rag_engine import RAGEngine
from mcp_support import MCPSupportEngine
import os

app = Flask(__name__)
rag_engine = RAGEngine()
mcp_engine = MCPSupportEngine()

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
        
        # Also initialize the MCP engine with the same data or use its own cache
        mcp_cache = "mcp_embeddings_cache.json"
        mcp_cache_loaded = False
        
        if os.path.exists(mcp_cache):
            print(f"Found MCP embeddings cache")
            # Assume MCP engine has a similar loading method
            if hasattr(mcp_engine, "load_embeddings"):
                mcp_cache_loaded = mcp_engine.load_embeddings(mcp_cache)
        
        if not mcp_cache_loaded:
            # Just use data loader for MCP engine
            from data_loader import load_gc_forms_data
            load_gc_forms_data(mcp_engine)
            
            # Save MCP embeddings if possible
            if hasattr(mcp_engine, "save_embeddings"):
                mcp_engine.save_embeddings(mcp_cache)
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
            <title>GC Forms RAG System (with Caching)</title>
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
                .cache-indicator { color: #388e3c; background: #e8f5e9; padding: 5px 10px; border-radius: 4px; font-size: 12px; }
                .hidden { display: none; }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>GC Forms RAG System <span class="cache-indicator">With Embedding Cache</span></h1>
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
                        <p><small>Using embedding cache for faster responses.</small></p>
                    </div>
                    <div id="results"></div>
                </div>
                
                <div id="api-content" class="tab-content hidden">
                    <div class="api-section">
                        <h2>API Endpoints</h2>
                        <p>This RAG system provides the following API endpoints for integration with MCP servers:</p>
                        
                        <div class="result-item">
                            <h3>Search Endpoint</h3>
                            <pre>POST /api/search</pre>
                            <p>Retrieve information from the knowledge base.</p>
                            <div class="metadata">
                                Request format: <code>{ "query": "your question here" }</code>
                            </div>
                        </div>
                        
                        <div class="result-item">
                            <h3>MCP Endpoint</h3>
                            <pre>POST /api/mcp</pre>
                            <p>Process a Model Context Protocol (MCP) request.</p>
                            <div class="metadata">
                                Compliant with MCP specification.
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="about-content" class="tab-content hidden">
                    <div class="api-section">
                        <h2>About This System</h2>
                        <p>This is a Retrieval-Augmented Generation (RAG) system for GC Forms. It uses:</p>
                        <ul>
                            <li>Vector embeddings for semantic search</li>
                            <li>Embedding cache for improved performance</li>
                            <li>Data from the Canada.ca Forms website and API documentation</li>
                            <li>MCP protocol support for integration with LLM systems</li>
                        </ul>
                        <p>This system demonstrates how to efficiently provide domain-specific knowledge to enhance question answering.</p>
                    </div>
                </div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Tab switching
                    const tabs = document.querySelectorAll('.tab');
                    const tabContents = document.querySelectorAll('.tab-content');
                    
                    tabs.forEach(tab => {
                        tab.addEventListener('click', function() {
                            const tabName = this.getAttribute('data-tab');
                            
                            // Deactivate all tabs and contents
                            tabs.forEach(t => t.classList.remove('active'));
                            tabContents.forEach(c => c.classList.add('hidden'));
                            
                            // Activate selected tab and content
                            this.classList.add('active');
                            document.querySelector(`#${tabName}-content`).classList.remove('hidden');
                        });
                    });
                    
                    // Form submission
                    document.getElementById('queryForm').addEventListener('submit', function(e) {
                        e.preventDefault();
                        
                        const query = document.getElementById('query').value;
                        if (!query.trim()) return;
                        
                        document.getElementById('results').innerHTML = 'Searching...';
                        
                        fetch('/api/search', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ query })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.results && data.results.length) {
                                let resultsHtml = `<h2>Results for: "${query}"</h2>`;
                                
                                data.results.forEach((result, index) => {
                                    resultsHtml += `
                                        <div class="result-item">
                                            <h3>Result ${index+1} <span class="similarity-badge">Match: ${(result.similarity * 100).toFixed(1)}%</span></h3>
                                            <p>${result.text}</p>
                                            <div class="metadata">
                                                Source: ${result.metadata.source || 'Unknown'}<br>
                                                ${result.metadata.url ? `URL: ${result.metadata.url}` : ''}
                                            </div>
                                        </div>
                                    `;
                                });
                                
                                document.getElementById('results').innerHTML = resultsHtml;
                            } else {
                                document.getElementById('results').innerHTML = '<p>No results found. Please try a different query.</p>';
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            document.getElementById('results').innerHTML = '<p>Error performing search. Please try again.</p>';
                        });
                    });
                });
            </script>
        </body>
    </html>
    """

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
        data = request.get_json()
        response = mcp_engine.process_mcp_request(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Initializing RAG system with caching...")
    initialize_data()
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
