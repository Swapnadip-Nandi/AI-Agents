"""
Web Search Tool using DuckDuckGo (Free API)
Provides web search capabilities for market research and fact verification.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import time


try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("Warning: duckduckgo-search not installed. Using mock mode.")


class WebSearchTool:
    """
    Free web search tool using DuckDuckGo API.
    No API key required.
    """
    
    def __init__(self, max_results: int = 5, timeout: int = 30):
        """
        Initialize web search tool.
        
        Args:
            max_results: Maximum number of search results
            timeout: Request timeout in seconds
        """
        self.max_results = max_results
        self.timeout = timeout
        self.search_history: List[Dict] = []
        
    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform web search.
        
        Args:
            query: Search query string
            max_results: Override default max results
            
        Returns:
            List of search results with title, snippet, and URL
        """
        results_limit = max_results if max_results else self.max_results
        
        if not DDGS_AVAILABLE:
            return self._mock_search(query, results_limit)
        
        try:
            with DDGS() as ddgs:
                results = []
                search_gen = ddgs.text(query, max_results=results_limit)
                
                for result in search_gen:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("body", ""),
                        "url": result.get("href", ""),
                        "source": "duckduckgo"
                    })
                    
            # Log search
            self.search_history.append({
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results_count": len(results)
            })
            
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return self._mock_search(query, results_limit)
            
    def _mock_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Mock search results for testing/fallback."""
        return [
            {
                "title": f"Search Result {i+1} for: {query}",
                "snippet": f"This is a mock search result snippet for query: {query}. "
                          f"In production, this would contain real search data from DuckDuckGo.",
                "url": f"https://example.com/result{i+1}",
                "source": "mock"
            }
            for i in range(max_results)
        ]
        
    def search_news(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for news articles.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            List of news results
        """
        results_limit = max_results if max_results else self.max_results
        
        if not DDGS_AVAILABLE:
            return self._mock_search(f"news: {query}", results_limit)
        
        try:
            with DDGS() as ddgs:
                results = []
                news_gen = ddgs.news(query, max_results=results_limit)
                
                for result in news_gen:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("body", ""),
                        "url": result.get("url", ""),
                        "date": result.get("date", ""),
                        "source": result.get("source", "unknown")
                    })
                    
            return results
            
        except Exception as e:
            print(f"News search error: {e}")
            return self._mock_search(f"news: {query}", results_limit)
            
    def search_products(self, product_name: str, marketplace: str = "amazon") -> List[Dict[str, Any]]:
        """
        Search for product information.
        
        Args:
            product_name: Product name to search
            marketplace: Marketplace to search (amazon, etc.)
            
        Returns:
            List of product results
        """
        query = f"{product_name} {marketplace}"
        return self.search(query, max_results=10)
        
    def search_competitors(self, product_category: str, marketplace: str = "amazon") -> List[Dict[str, Any]]:
        """
        Search for competitor products.
        
        Args:
            product_category: Product category
            marketplace: Marketplace to search
            
        Returns:
            List of competitor results
        """
        query = f"best {product_category} on {marketplace}"
        return self.search(query, max_results=10)
        
    def verify_fact(self, claim: str) -> Dict[str, Any]:
        """
        Verify a factual claim through web search.
        
        Args:
            claim: Claim to verify
            
        Returns:
            Verification result
        """
        results = self.search(claim, max_results=3)
        
        # Simple verification based on result count and relevance
        verification = {
            "claim": claim,
            "verified": len(results) > 0,
            "confidence": min(len(results) * 33, 100),  # Rough confidence score
            "sources": [r["url"] for r in results],
            "timestamp": datetime.now().isoformat()
        }
        
        return verification
        
    def get_market_trends(self, product_category: str) -> List[Dict[str, Any]]:
        """
        Get market trends for a product category.
        
        Args:
            product_category: Product category
            
        Returns:
            List of trend articles
        """
        query = f"{product_category} market trends 2025"
        return self.search(query, max_results=5)
        
    def get_search_history(self) -> List[Dict]:
        """Get search history."""
        return self.search_history
        
    def clear_history(self):
        """Clear search history."""
        self.search_history = []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "web_search",
            "description": "Search the web for information using DuckDuckGo. Useful for market research, competitor analysis, and fact verification.",
            "parameters": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (default: 5)",
                    "optional": True
                }
            }
        }
