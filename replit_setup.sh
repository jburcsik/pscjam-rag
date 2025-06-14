#!/bin/bash

# Ensure static directory exists
mkdir -p static

# Make sure our HTML file exists for testing the API
if [ ! -f "static/index.html" ]; then
  echo "Creating index.html for API testing..."
  cat > static/index.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GC Forms RAG API</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            line-height: 1.6;
            color: #333;
            background: #f7f9fc;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }
        h1 {
            color: #4285f4;
            margin-top: 0;
        }
        .query-box {
            margin: 20px 0;
        }
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            min-height: 100px;
        }
        button {
            padding: 10px 20px;
            background: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #3b78e7;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f1f3f4;
            border-radius: 4px;
            white-space: pre-wrap;
            overflow-wrap: break-word;
        }
        .api-info {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }
        .code {
            background: #f1f3f4;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GC Forms RAG API Tester</h1>
        <p>This tool allows you to query the GC Forms RAG system directly from your browser.</p>
        
        <div class="query-box">
            <h3>Enter your query:</h3>
            <textarea id="queryInput" placeholder="e.g., How do I authenticate with the GC Forms API?"></textarea>
            <div style="margin-top: 10px;">
                <button id="submitBtn">Submit Query</button>
            </div>
        </div>
        
        <div id="resultContainer" style="display: none;">
            <h3>Results:</h3>
            <div id="resultOutput" class="result"></div>
        </div>
        
        <div class="api-info">
            <h2>API Documentation</h2>
            <p>To integrate with this API programmatically, use the following endpoint:</p>
            
            <h3>Query Endpoint</h3>
            <p class="code">POST /query</p>
            <p>Send a JSON object with a "query" field:</p>
            <div class="code">{
  "query": "How do I authenticate with the GC Forms API?"
}</div>
            
            <h3>Sample Code (Python)</h3>
            <div class="code">import requests
import json

url = "https://pscjam-rag-1.jesseburcsik.repl.co/query"
payload = {"query": "How do I authenticate with the GC Forms API?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(payload))
data = response.json()
print(data["results"])
</div>
            
            <h3>Sample Code (JavaScript)</h3>
            <div class="code">fetch('https://pscjam-rag-1.jesseburcsik.repl.co/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'How do I authenticate with the GC Forms API?',
  }),
})
.then(response => response.json())
.then(data => {
  console.log(data.results);
});
</div>
        </div>
    </div>
    
    <script>
        document.getElementById('submitBtn').addEventListener('click', async () => {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) return;
            
            // Show loading state
            document.getElementById('submitBtn').textContent = 'Loading...';
            document.getElementById('submitBtn').disabled = true;
            
            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query }),
                });
                
                const data = await response.json();
                
                // Format and display the results
                const resultContainer = document.getElementById('resultContainer');
                const resultOutput = document.getElementById('resultOutput');
                
                if (data.results && data.results.length > 0) {
                    let html = '';
                    data.results.forEach((result, index) => {
                        html += `<div style="margin-bottom: 20px;">
                            <p><strong>Result ${index + 1}</strong> (Similarity: ${(result.similarity * 100).toFixed(1)}%)</p>
                            <p>${result.text}</p>
                            <p><small>Source: ${result.metadata?.source || 'Unknown'}</small></p>
                        </div>`;
                    });
                    resultOutput.innerHTML = html;
                } else {
                    resultOutput.innerHTML = '<p>No results found. Try a different query.</p>';
                }
                
                resultContainer.style.display = 'block';
            } catch (error) {
                document.getElementById('resultOutput').innerHTML = `<p>Error: ${error.message}</p>`;
                document.getElementById('resultContainer').style.display = 'block';
            }
            
            # Reset button
            document.getElementById('submitBtn').textContent = 'Submit Query';
            document.getElementById('submitBtn').disabled = false;
        });
    </script>
</body>
</html>
EOL
fi

# Verify that the `.env` file or environment variables are set up
if [ ! -f ".env" ] && [ -z "$OPENAI_API_KEY" ]; then
  echo "Warning: No .env file found and OPENAI_API_KEY environment variable is not set."
  echo "Please set your OpenAI API key in the Replit Secrets tab."
  echo "Creating a sample .env file..."
  
  # Create a template .env file
  echo "OPENAI_API_KEY=your_api_key_here" > .env
  echo "OPENAI_API_BASE=https://api.openai.com/v1/embeddings" >> .env
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the Flask application
echo "Starting the GC Forms RAG API server..."
python app.py
