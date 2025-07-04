# web_scraper.py
"""
Web Scraper Utility Module

A simple, reusable web scraping utility for extracting text content from websites.

Usage:
    from utils.web_scraper import WebScraper
    
    scraper = WebScraper()
    text = scraper.scrape_url("https://example.com")
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
from urllib.parse import urlparse
from typing import Optional, List, Union
import logging

class WebScraper:
    """
    A simple web scraper utility for extracting text content from websites.
    
    Attributes:
        delay (float): Delay between requests in seconds
        timeout (int): Request timeout in seconds
        output_dir (str): Default output directory for saved files
    """
    
    def __init__(self, delay: float = 1.0, timeout: int = 30, output_dir: str = "scraped_content"):
        """
        Initialize the web scraper.
        
        Args:
            delay: Delay between requests in seconds (default: 1.0)
            timeout: Request timeout in seconds (default: 30)
            output_dir: Default output directory (default: "scraped_content")
        """
        self.delay = delay
        self.timeout = timeout
        self.output_dir = output_dir
        
        # Setup session with browser-like headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def scrape_url(self, url: str, save_to_file: bool = True, custom_output_dir: Optional[str] = None) -> Optional[str]:
        """
        Scrape text content from a single URL.
        
        Args:
            url: Website URL to scrape
            save_to_file: Whether to save content to file (default: True)
            custom_output_dir: Custom output directory (optional)
            
        Returns:
            Extracted text content or None if failed
        """
        try:
            self.logger.info(f"Scraping: {url}")
            
            # Make request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse and extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            text = self._extract_text(soup)
            
            # Save to file if requested
            if save_to_file and text:
                output_dir = custom_output_dir or self.output_dir
                self._save_text_file(text, url, output_dir)
            
            # Respectful delay
            time.sleep(self.delay)
            
            return text
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def scrape_multiple_urls(self, urls: List[str], save_to_files: bool = True, 
                           custom_output_dir: Optional[str] = None) -> List[str]:
        """
        Scrape multiple URLs and return list of extracted texts.
        
        Args:
            urls: List of URLs to scrape
            save_to_files: Whether to save content to files (default: True)
            custom_output_dir: Custom output directory (optional)
            
        Returns:
            List of extracted text contents (empty string for failed scrapes)
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Processing {i}/{len(urls)}: {url}")
            
            text = self.scrape_url(url, save_to_files, custom_output_dir)
            results.append(text or "")
        
        return results
    
    def get_text_only(self, url: str) -> Optional[str]:
        """
        Scrape URL and return only text content without saving to file.
        
        Args:
            url: Website URL to scrape
            
        Returns:
            Extracted text content or None if failed
        """
        return self.scrape_url(url, save_to_file=False)
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """
        Extract and clean text from BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup parsed HTML
            
        Returns:
            Cleaned text content
        """
        # Remove unwanted elements
        unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 
                        'form', 'button', 'input', 'select', 'textarea']
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Extract text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean text
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and formatting.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _save_text_file(self, text: str, url: str, output_dir: str) -> str:
        """
        Save text content to file.
        
        Args:
            text: Text content to save
            url: Source URL
            output_dir: Output directory
            
        Returns:
            Path to saved file
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        filename = self._generate_filename(url)
        file_path = os.path.join(output_dir, filename)
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Scraped: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Content Length: {len(text)} characters\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        
        self.logger.info(f"Saved: {file_path} ({len(text)} characters)")
        return file_path
    
    def _generate_filename(self, url: str) -> str:
        """
        Generate filename from URL.
        
        Args:
            url: Source URL
            
        Returns:
            Generated filename
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')
        
        # Create base filename
        filename = f"{domain}_{int(time.time())}.txt"
        
        # Clean filename
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        
        return filename
    
    def set_delay(self, delay: float) -> None:
        """Set delay between requests."""
        self.delay = delay
    
    def set_timeout(self, timeout: int) -> None:
        """Set request timeout."""
        self.timeout = timeout
    
    def set_output_dir(self, output_dir: str) -> None:
        """Set default output directory."""
        self.output_dir = output_dir


# Convenience functions for quick usage
def scrape_url(url: str, output_dir: str = "scraped_content") -> Optional[str]:
    """
    Quick function to scrape a single URL.
    
    Args:
        url: Website URL to scrape
        output_dir: Output directory
        
    Returns:
        Extracted text or None if failed
    """
    scraper = WebScraper(output_dir=output_dir)
    return scraper.scrape_url(url)

def scrape_multiple_urls(urls: List[str], output_dir: str = "scraped_content") -> List[str]:
    """
    Quick function to scrape multiple URLs.
    
    Args:
        urls: List of URLs to scrape
        output_dir: Output directory
        
    Returns:
        List of extracted texts
    """
    scraper = WebScraper(output_dir=output_dir)
    return scraper.scrape_multiple_urls(urls)

def get_text_from_url(url: str) -> Optional[str]:
    """
    Quick function to get text from URL without saving to file.
    
    Args:
        url: Website URL to scrape
        
    Returns:
        Extracted text or None if failed
    """
    scraper = WebScraper()
    return scraper.get_text_only(url)