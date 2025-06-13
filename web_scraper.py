"""
Web scraper module for collecting content from Canada.ca forms website.
"""
import requests
from bs4 import BeautifulSoup
import time
import os
import json

class WebScraper:
    """A scraper for the Canada.ca Forms website and its subpages."""
    
    def __init__(self, base_url="https://articles.alpha.canada.ca/forms-formulaires/"):
        """Initialize the scraper with a base URL."""
        self.base_url = base_url
        self.visited_urls = set()
        self.collected_content = []
        
    def _normalize_url(self, url):
        """Normalize a URL to avoid duplicates."""
        # Remove trailing slash if present
        if url.endswith('/'):
            url = url[:-1]
        # Ensure URL has the correct domain
        if url.startswith('/'):
            url = self.base_url + url[1:] if self.base_url.endswith('/') else self.base_url + url
        return url
    
    def _is_valid_url(self, url):
        """Check if a URL is valid for scraping."""
        # Only process URLs from the same domain
        if not url.startswith(self.base_url) and not url.startswith('/'):
            return False
        # Skip URLs we've already visited
        normalized = self._normalize_url(url)
        if normalized in self.visited_urls:
            return False
        # Skip certain file types or patterns
        skip_extensions = ['.pdf', '.jpg', '.png', '.gif', '.zip', '.doc', '.docx']
        if any(url.endswith(ext) for ext in skip_extensions):
            return False
        return True
    
    def _extract_page_content(self, url):
        """Extract content from a single page."""
        try:
            print(f"Fetching: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error fetching URL: {url}, status code: {response.status_code}")
                return None, []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract useful content sections
            content_sections = soup.select('main, article, .content, .page-content')
            
            # If no content sections found, try the whole body
            if not content_sections:
                content_sections = [soup.body] if soup.body else []
            
            # Extract text from content sections
            content = ""
            for section in content_sections:
                # Remove script and style elements
                for element in section(['script', 'style']):
                    element.decompose()
                # Get the text
                section_text = section.get_text(separator='\n').strip()
                content += section_text + "\n\n"
            
            # Extract title
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.string.strip()
            
            # Extract links for further scraping
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if self._is_valid_url(href):
                    # Normalize URL
                    normalized_url = self._normalize_url(href)
                    links.append(normalized_url)
            
            # Create document metadata
            metadata = {
                "source": "Canada.ca Forms Website",
                "url": url,
                "title": title,
                "section": "website_content"
            }
            
            # Add document to collection
            if content.strip():
                self.collected_content.append({
                    "text": content,
                    "metadata": metadata
                })
                print(f"Extracted content from: {url} - Title: {title}")
                
            return content, links
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            return None, []
    
    def scrape(self, max_pages=30, delay=1):
        """
        Scrape content from the website and its subpages.
        
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
            
            # Respect robots.txt with a delay
            if delay > 0:
                time.sleep(delay)
                
        print(f"Scraping complete. Visited {len(self.visited_urls)} pages.")
        print(f"Collected {len(self.collected_content)} documents.")
        
        return self.collected_content
    
    def save_to_file(self, filename="canada_forms_content.json"):
        """Save collected content to a JSON file."""
        if not self.collected_content:
            print("No content collected to save.")
            return
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.collected_content, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(self.collected_content)} documents to {filename}")

def scrape_canada_forms_website(max_pages=30):
    """
    Scrape the Canada.ca Forms website and return the collected documents.
    
    Args:
        max_pages: Maximum number of pages to scrape
        
    Returns:
        list: List of collected documents with text and metadata
    """
    scraper = WebScraper()
    documents = scraper.scrape(max_pages=max_pages)
    scraper.save_to_file()
    return documents

if __name__ == "__main__":
    # When run as a script, scrape the website and save results
    scrape_canada_forms_website()
