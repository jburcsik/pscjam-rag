"""
API documentation site scraper for forms.ai-jam.cdssandbox.xyz.
"""
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re

class ApiDocScraper:
    """A scraper for the Forms API documentation website."""
    
    def __init__(self, base_url="https://forms.ai-jam.cdssandbox.xyz"):
        """Initialize the scraper with a base URL."""
        self.base_url = base_url
        self.visited_urls = set()
        self.collected_content = []
        
    def _normalize_url(self, url):
        """Normalize a URL to avoid duplicates."""
        # Remove trailing slash if present
        if url.endswith('/'):
            url = url[:-1]
        # Make relative URLs absolute
        if url.startswith('/'):
            url = self.base_url + url
        # Handle URLs without scheme
        if not url.startswith('http'):
            if url.startswith('/'):
                url = self.base_url + url
            else:
                url = f"{self.base_url}/{url}"
        return url
    
    def _is_valid_url(self, url):
        """Check if a URL is valid for scraping."""
        # Skip external URLs
        if not url.startswith(self.base_url) and not url.startswith('/'):
            return False
        # Skip already visited URLs
        normalized = self._normalize_url(url)
        if normalized in self.visited_urls:
            return False
        # Skip file extensions we're not interested in
        skip_extensions = ['.pdf', '.jpg', '.png', '.gif', '.zip', '.css', '.js']
        if any(url.endswith(ext) for ext in skip_extensions):
            return False
        return True
    
    def _extract_page_content(self, url):
        """Extract content from a single page."""
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Error fetching URL: {url}, status code: {response.status_code}")
                return None, []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.text.strip() if title_tag else "No title"
            
            # Extract API documentation content - focus on main content areas
            content_sections = soup.select('main, article, .content, .documentation, .api-docs, .markdown-body')
            
            if not content_sections:
                # Fallback to common content containers
                content_sections = soup.select('.container, .content-wrapper, #content, .page-content')
            
            if not content_sections:
                # Last resort, use the body
                content_sections = [soup.body] if soup.body else []
            
            # Clean and extract text from content sections
            content = ""
            for section in content_sections:
                # Remove script, style, and nav elements
                for element in section.select('script, style, nav, footer'):
                    element.decompose()
                
                # Get cleaned text
                section_text = section.get_text(separator='\n', strip=True)
                content += section_text + "\n\n"
            
            # Extract links for further scraping
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if self._is_valid_url(href):
                    normalized_url = self._normalize_url(href)
                    links.append(normalized_url)
            
            # Extract API endpoints and methods if present
            api_endpoints = []
            
            # Look for API method signatures (common in API docs)
            method_patterns = [
                soup.select('.endpoint, .api-endpoint, .method-signature'),
                soup.select('code:not(pre code)'),
                soup.find_all(string=re.compile(r'GET|POST|PUT|DELETE|PATCH.*?/api/'))
            ]
            
            for pattern_matches in method_patterns:
                for element in pattern_matches:
                    api_text = element.get_text(strip=True) if hasattr(element, 'get_text') else str(element)
                    api_endpoints.append(api_text)
            
            # Create document metadata
            metadata = {
                "source": "Forms API Documentation",
                "url": url,
                "title": title,
                "section": "api_docs",
                "api_endpoints": api_endpoints if api_endpoints else []
            }
            
            # Add document to collection if we have content
            if content.strip():
                self.collected_content.append({
                    "text": content,
                    "metadata": metadata
                })
                print(f"Extracted content from: {url} - Title: {title}")
                print(f"Found {len(api_endpoints)} API endpoint references")
            else:
                print(f"No content extracted from: {url}")
                
            return content, links
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            return None, []
    
    def scrape(self, max_pages=30, delay=1):
        """
        Scrape content from the API documentation site.
        
        Args:
            max_pages: Maximum number of pages to scrape
            delay: Delay between requests in seconds
            
        Returns:
            list: List of collected documents with text and metadata
        """
        print(f"Starting to scrape {self.base_url}")
        print(f"Will collect up to {max_pages} pages")
        
        # Start with base URL
        to_visit = [self.base_url]
        
        # Process URLs until we reach the limit or run out of URLs
        page_count = 0
        while to_visit and page_count < max_pages:
            # Get the next URL
            url = to_visit.pop(0)
            normalized_url = self._normalize_url(url)
            
            # Skip if already visited
            if normalized_url in self.visited_urls:
                continue
            
            # Mark as visited
            self.visited_urls.add(normalized_url)
            
            # Extract content and links
            _, links = self._extract_page_content(normalized_url)
            
            # Add new links to visit
            for link in links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
            
            # Increment counter
            page_count += 1
            
            # Respect site with a delay
            if delay > 0:
                time.sleep(delay)
                
        print(f"Scraping complete. Visited {len(self.visited_urls)} pages.")
        print(f"Collected {len(self.collected_content)} documents.")
        
        return self.collected_content
    
    def save_to_file(self, filename="api_docs_content.json"):
        """Save collected content to a JSON file."""
        if not self.collected_content:
            print("No content collected to save.")
            return
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_content, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(self.collected_content)} documents to {filename}")

def scrape_api_documentation(max_pages=30):
    """
    Scrape the Forms API documentation site and return the collected documents.
    
    Args:
        max_pages: Maximum number of pages to scrape
        
    Returns:
        list: List of collected documents with text and metadata
    """
    scraper = ApiDocScraper()
    documents = scraper.scrape(max_pages=max_pages)
    scraper.save_to_file()
    return documents

if __name__ == "__main__":
    # When run as a script, scrape the website and save results
    print("Starting API documentation scraping...")
    try:
        docs = scrape_api_documentation()
        print(f"Completed scraping with {len(docs)} documents")
    except Exception as e:
        import traceback
        print(f"Error during scraping: {str(e)}")
        traceback.print_exc()
