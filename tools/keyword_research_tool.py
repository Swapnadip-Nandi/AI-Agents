"""
Keyword Research Tool (Free/Open Source)
Provides SEO keyword research using free APIs and web scraping.
"""

from typing import Any, Dict, List, Optional
import re
from datetime import datetime


class KeywordResearchTool:
    """
    Free keyword research tool for SEO optimization.
    Uses algorithmic approach and web data for keyword suggestions.
    """
    
    def __init__(self):
        """Initialize keyword research tool."""
        self.keyword_history: List[Dict] = []
        
    def generate_keywords(self, seed_keyword: str, product_category: str) -> List[Dict[str, Any]]:
        """
        Generate keyword suggestions.
        
        Args:
            seed_keyword: Base keyword
            product_category: Product category
            
        Returns:
            List of keyword suggestions with metrics
        """
        keywords = []
        
        # Generate variations
        variations = self._generate_variations(seed_keyword, product_category)
        
        for keyword in variations:
            keywords.append({
                "keyword": keyword,
                "search_volume": self._estimate_search_volume(keyword),
                "competition": self._estimate_competition(keyword),
                "relevance": self._calculate_relevance(keyword, seed_keyword),
                "keyword_type": self._classify_keyword(keyword)
            })
            
        # Sort by relevance and search volume
        keywords.sort(key=lambda x: (x["relevance"], x["search_volume"]), reverse=True)
        
        # Log research
        self.keyword_history.append({
            "seed_keyword": seed_keyword,
            "timestamp": datetime.now().isoformat(),
            "keywords_found": len(keywords)
        })
        
        return keywords[:20]  # Return top 20
        
    def _generate_variations(self, seed: str, category: str) -> List[str]:
        """Generate keyword variations."""
        variations = [seed]
        
        # Add category-based variations
        variations.extend([
            f"{seed} {category}",
            f"best {seed}",
            f"{seed} for {category}",
            f"top {seed}",
            f"{seed} reviews",
            f"buy {seed}",
            f"{seed} online",
            f"cheap {seed}",
            f"affordable {seed}",
            f"{seed} deals",
            f"{seed} sale",
            f"premium {seed}",
            f"professional {seed}",
            f"{seed} brands",
            f"{seed} comparison"
        ])
        
        # Add question-based keywords
        variations.extend([
            f"what is {seed}",
            f"how to use {seed}",
            f"why buy {seed}",
            f"where to buy {seed}",
            f"when to use {seed}"
        ])
        
        # Add long-tail variations
        variations.extend([
            f"{seed} with high quality",
            f"{seed} that lasts",
            f"{seed} with warranty",
            f"{seed} with free shipping",
            f"{seed} for beginners"
        ])
        
        return list(set(variations))  # Remove duplicates
        
    def _estimate_search_volume(self, keyword: str) -> int:
        """Estimate monthly search volume."""
        # Simple heuristic based on keyword characteristics
        base_volume = 1000
        
        # Shorter keywords typically have higher volume
        length_factor = max(1, 5 - len(keyword.split()))
        
        # Generic terms have higher volume
        generic_terms = ["best", "top", "cheap", "buy"]
        generic_boost = 1.5 if any(term in keyword.lower() for term in generic_terms) else 1.0
        
        # Long-tail keywords have lower volume
        is_long_tail = len(keyword.split()) > 4
        long_tail_penalty = 0.3 if is_long_tail else 1.0
        
        estimated = int(base_volume * length_factor * generic_boost * long_tail_penalty)
        
        return max(100, min(estimated, 100000))  # Clamp between 100 and 100k
        
    def _estimate_competition(self, keyword: str) -> str:
        """Estimate keyword competition level."""
        word_count = len(keyword.split())
        
        # Short, generic keywords = high competition
        if word_count <= 2:
            return "high"
        elif word_count <= 4:
            return "medium"
        else:
            return "low"
            
    def _calculate_relevance(self, keyword: str, seed: str) -> float:
        """Calculate relevance score (0-1)."""
        keyword_lower = keyword.lower()
        seed_lower = seed.lower()
        
        # Exact match = highest relevance
        if seed_lower == keyword_lower:
            return 1.0
            
        # Contains seed = high relevance
        if seed_lower in keyword_lower:
            # Shorter variations are more relevant
            length_ratio = len(seed_lower) / len(keyword_lower)
            return 0.7 + (length_ratio * 0.3)
            
        # Word overlap
        seed_words = set(seed_lower.split())
        keyword_words = set(keyword_lower.split())
        overlap = len(seed_words & keyword_words) / len(seed_words)
        
        return overlap * 0.6
        
    def _classify_keyword(self, keyword: str) -> str:
        """Classify keyword type."""
        keyword_lower = keyword.lower()
        
        if any(q in keyword_lower for q in ["what", "how", "why", "where", "when"]):
            return "informational"
        elif any(t in keyword_lower for t in ["buy", "price", "cheap", "deal", "sale"]):
            return "transactional"
        elif any(c in keyword_lower for c in ["vs", "compare", "best", "top", "review"]):
            return "commercial"
        else:
            return "navigational"
            
    def analyze_keyword_difficulty(self, keyword: str) -> Dict[str, Any]:
        """
        Analyze keyword difficulty.
        
        Args:
            keyword: Keyword to analyze
            
        Returns:
            Difficulty analysis
        """
        word_count = len(keyword.split())
        competition = self._estimate_competition(keyword)
        
        # Calculate difficulty score (0-100)
        if competition == "high":
            difficulty = 70 + (min(word_count, 2) * 10)
        elif competition == "medium":
            difficulty = 40 + (word_count * 5)
        else:
            difficulty = 10 + (word_count * 3)
            
        difficulty = min(difficulty, 100)
        
        return {
            "keyword": keyword,
            "difficulty_score": difficulty,
            "competition": competition,
            "recommendation": "target" if difficulty < 60 else "consider" if difficulty < 80 else "avoid",
            "word_count": word_count,
            "estimated_time_to_rank": "1-3 months" if difficulty < 40 else "3-6 months" if difficulty < 70 else "6+ months"
        }
        
    def get_long_tail_keywords(self, seed: str, category: str, min_words: int = 4) -> List[str]:
        """
        Get long-tail keyword suggestions.
        
        Args:
            seed: Seed keyword
            category: Product category
            min_words: Minimum word count for long-tail
            
        Returns:
            List of long-tail keywords
        """
        all_keywords = self.generate_keywords(seed, category)
        long_tail = [
            kw["keyword"] for kw in all_keywords
            if len(kw["keyword"].split()) >= min_words
        ]
        return long_tail
        
    def get_primary_keywords(self, seed: str, category: str, max_count: int = 5) -> List[str]:
        """
        Get primary keyword recommendations.
        
        Args:
            seed: Seed keyword
            category: Product category  
            max_count: Maximum number of keywords
            
        Returns:
            List of primary keywords
        """
        all_keywords = self.generate_keywords(seed, category)
        
        # Filter for high-volume, medium competition
        primary = [
            kw["keyword"] for kw in all_keywords
            if kw["competition"] in ["medium", "low"] and kw["relevance"] > 0.7
        ]
        
        return primary[:max_count]
        
    def get_secondary_keywords(self, seed: str, category: str, max_count: int = 10) -> List[str]:
        """
        Get secondary keyword recommendations.
        
        Args:
            seed: Seed keyword
            category: Product category
            max_count: Maximum number of keywords
            
        Returns:
            List of secondary keywords
        """
        all_keywords = self.generate_keywords(seed, category)
        
        # Filter for medium relevance
        secondary = [
            kw["keyword"] for kw in all_keywords
            if 0.4 < kw["relevance"] <= 0.7
        ]
        
        return secondary[:max_count]
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "keyword_research",
            "description": "Research SEO keywords for product optimization. Generates keyword suggestions with search volume and competition estimates.",
            "parameters": {
                "seed_keyword": {
                    "type": "string",
                    "description": "Base keyword to research"
                },
                "product_category": {
                    "type": "string",
                    "description": "Product category for context"
                }
            }
        }
