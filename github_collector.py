"""
GitHub repository data collector for the Platform Forms client repository.
"""
import requests
import os
import json
import base64
import time
from urllib.parse import urljoin

class GitHubRepoCollector:
    """A collector for GitHub repository content, focusing on documentation."""
    
    def __init__(self, repo="cds-snc/platform-forms-client", api_base="https://api.github.com"):
        """Initialize the collector with a repository name."""
        self.repo = repo
        self.api_base = api_base
        self.collected_content = []
        self.api_url = f"{api_base}/repos/{repo}/contents"
        
        # Important file patterns to extract content from
        self.doc_patterns = [
            'README', '.md', 'CONTRIBUTING', 'SECURITY', 'LICENSE',
            'docs/', '.txt', 'package.json', 'CHANGELOG'
        ]
        
        # Files to ignore
        self.ignore_patterns = [
            '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', 
            '.min.js', '.css', '.lock', '.gitignore', '.gitmodules',
            'node_modules/', 'dist/', 'build/'
        ]

        # Track API rate limiting
        self.remaining_api_calls = 60  # GitHub's default unauthenticated rate limit
        self.reset_time = None
    
    def _check_rate_limit(self):
        """Check if we're approaching rate limits and handle accordingly."""
        if self.remaining_api_calls < 5:
            wait_time = self.reset_time - time.time() if self.reset_time else 60
            if wait_time > 0:
                print(f"Approaching rate limit. Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time + 1)
    
    def _update_rate_limit(self, headers):
        """Update rate limit tracking based on API response headers."""
        if 'X-RateLimit-Remaining' in headers:
            self.remaining_api_calls = int(headers['X-RateLimit-Remaining'])
        if 'X-RateLimit-Reset' in headers:
            self.reset_time = int(headers['X-RateLimit-Reset'])
    
    def _is_doc_file(self, path):
        """Check if a file path looks like documentation."""
        path_lower = path.lower()
        return any(pattern.lower() in path_lower for pattern in self.doc_patterns)
    
    def _should_ignore(self, path):
        """Check if a file path should be ignored."""
        path_lower = path.lower()
        return any(pattern.lower() in path_lower for pattern in self.ignore_patterns)
    
    def _process_file_content(self, file_data):
        """Process and extract content from a file."""
        try:
            if file_data.get('type') != 'file':
                return
                
            file_name = file_data.get('name', '')
            file_path = file_data.get('path', '')
            
            # Skip binary files or files we don't want
            if self._should_ignore(file_path):
                return
                
            # For documentation files, extract content
            if self._is_doc_file(file_path):
                print(f"Processing file: {file_path}")
                
                # Get file content
                if 'download_url' in file_data and file_data['download_url']:
                    response = requests.get(file_data['download_url'])
                    if response.status_code == 200:
                        content = response.text
                    else:
                        print(f"Error downloading {file_path}: {response.status_code}")
                        return
                elif 'content' in file_data and file_data['content']:
                    # Content is base64 encoded
                    content = base64.b64decode(file_data['content']).decode('utf-8', errors='replace')
                else:
                    print(f"No content available for {file_path}")
                    return
                
                # Create document metadata
                metadata = {
                    "source": "GitHub Repository",
                    "repo": self.repo,
                    "file_path": file_path,
                    "file_name": file_name,
                    "section": "technical_docs"
                }
                
                # Add document to collection
                self.collected_content.append({
                    "text": content,
                    "metadata": metadata
                })
                print(f"Added content from: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_data.get('path', 'unknown')}: {str(e)}")
    
    def _process_directory(self, path=""):
        """Recursively process a directory in the repository."""
        url = urljoin(self.api_url + "/", path)
        
        try:
            self._check_rate_limit()
            response = requests.get(url)
            self._update_rate_limit(response.headers)
            
            if response.status_code != 200:
                print(f"Error fetching directory {path}: {response.status_code}")
                return
                
            contents = response.json()
            
            for item in contents:
                item_type = item.get('type')
                item_path = item.get('path', '')
                
                # Skip ignored paths
                if self._should_ignore(item_path):
                    continue
                    
                # Process files
                if item_type == 'file':
                    self._process_file_content(item)
                    
                # Recursively process directories
                elif item_type == 'dir':
                    self._process_directory(item_path)
                    
        except Exception as e:
            print(f"Error processing directory {path}: {str(e)}")
    
    def collect(self):
        """
        Collect content from the GitHub repository.
        
        Returns:
            list: List of collected documents with text and metadata
        """
        print(f"Collecting content from GitHub repository: {self.repo}")
        self._process_directory()
        print(f"Collection complete. Collected {len(self.collected_content)} documents.")
        return self.collected_content
    
    def save_to_file(self, filename="github_repo_content.json"):
        """Save collected content to a JSON file."""
        if not self.collected_content:
            print("No content collected to save.")
            return
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_content, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(self.collected_content)} documents to {filename}")

def collect_github_repo_data():
    """
    Collect documentation from the Platform Forms client repository.
    
    Returns:
        list: List of collected documents with text and metadata
    """
    collector = GitHubRepoCollector()
    documents = collector.collect()
    collector.save_to_file()
    return documents

if __name__ == "__main__":
    # When run as a script, collect repository content and save results
    collect_github_repo_data()
