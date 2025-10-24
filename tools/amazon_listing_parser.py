"""
Amazon Listing Parser (Custom Tool)
Parses and analyzes Amazon product listings for optimization.
"""

from typing import Any, Dict, List, Optional
import re


class AmazonListingParser:
    """
    Custom tool for parsing and analyzing Amazon product listings.
    Validates listing format and extracts key components.
    """
    
    def __init__(self):
        """Initialize parser."""
        self.character_limits = {
            "title": 200,
            "bullet_point": 500,
            "description": 2000,
            "search_terms": 250
        }
        
    def parse_listing(self, listing_text: str) -> Dict[str, Any]:
        """
        Parse a complete Amazon listing.
        
        Args:
            listing_text: Raw listing text
            
        Returns:
            Parsed listing components
        """
        # Simple parsing logic
        sections = {
            "title": "",
            "bullet_points": [],
            "description": "",
            "search_terms": [],
            "brand": "",
            "price": None
        }
        
        # Extract title (usually first line or marked)
        lines = listing_text.split('\n')
        for line in lines:
            if line.strip() and not sections["title"]:
                sections["title"] = line.strip()
                break
                
        return sections
        
    def validate_title(self, title: str) -> Dict[str, Any]:
        """
        Validate product title.
        
        Args:
            title: Product title
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        # Check length
        if len(title) > self.character_limits["title"]:
            issues.append(f"Title exceeds {self.character_limits['title']} characters")
        elif len(title) < 50:
            warnings.append("Title is too short (recommended: 80-200 characters)")
            
        # Check for prohibited content
        prohibited = ["amazon", "prime", "best seller", "free shipping"]
        for term in prohibited:
            if term.lower() in title.lower():
                issues.append(f"Prohibited term '{term}' found in title")
                
        # Check capitalization
        if title.isupper():
            issues.append("Title should not be all uppercase")
            
        # Check for excessive punctuation
        if title.count('!') > 1 or title.count('?') > 1:
            warnings.append("Excessive punctuation detected")
            
        return {
            "valid": len(issues) == 0,
            "length": len(title),
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - (len(issues) * 25) - (len(warnings) * 10))
        }
        
    def validate_bullet_points(self, bullet_points: List[str]) -> Dict[str, Any]:
        """
        Validate bullet points.
        
        Args:
            bullet_points: List of bullet points
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        # Check count
        if len(bullet_points) < 3:
            warnings.append("Recommended to have 5 bullet points")
        elif len(bullet_points) > 5:
            issues.append("Maximum 5 bullet points allowed")
            
        # Check each bullet point
        for i, bullet in enumerate(bullet_points):
            if len(bullet) > self.character_limits["bullet_point"]:
                issues.append(f"Bullet point {i+1} exceeds {self.character_limits['bullet_point']} characters")
            elif len(bullet) < 50:
                warnings.append(f"Bullet point {i+1} is too short")
                
            # Check for prohibited content
            if "price" in bullet.lower() or "$" in bullet:
                issues.append(f"Bullet point {i+1} contains pricing information")
                
        return {
            "valid": len(issues) == 0,
            "count": len(bullet_points),
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - (len(issues) * 20) - (len(warnings) * 5))
        }
        
    def validate_description(self, description: str) -> Dict[str, Any]:
        """
        Validate product description.
        
        Args:
            description: Product description
            
        Returns:
            Validation result
        """
        issues = []
        warnings = []
        
        # Check length
        if len(description) > self.character_limits["description"]:
            issues.append(f"Description exceeds {self.character_limits['description']} characters")
        elif len(description) < 200:
            warnings.append("Description is too short")
            
        # Check for HTML tags (allowed in descriptions)
        html_tags = re.findall(r'<[^>]+>', description)
        if html_tags:
            # Validate allowed tags
            allowed_tags = ['b', 'i', 'u', 'br', 'p', 'ul', 'li', 'ol']
            for tag in html_tags:
                tag_name = re.search(r'</?(\w+)', tag)
                if tag_name and tag_name.group(1).lower() not in allowed_tags:
                    warnings.append(f"Potentially unsupported HTML tag: {tag}")
                    
        return {
            "valid": len(issues) == 0,
            "length": len(description),
            "contains_html": len(html_tags) > 0,
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - (len(issues) * 25) - (len(warnings) * 10))
        }
        
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from listing text.
        
        Args:
            text: Listing text
            
        Returns:
            List of extracted keywords
        """
        # Simple keyword extraction
        text = text.lower()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'for', 'to', 'of', 'on', 'at', 'by', 'from'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', text)
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Count frequency
        keyword_freq = {}
        for kw in keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
            
        # Sort by frequency
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [kw for kw, _ in sorted_keywords[:20]]
        
    def analyze_listing_completeness(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze if listing is complete.
        
        Args:
            listing: Listing dictionary
            
        Returns:
            Completeness analysis
        """
        required_fields = ["title", "bullet_points", "description"]
        optional_fields = ["search_terms", "brand", "images"]
        
        completeness = {
            "complete": True,
            "missing_required": [],
            "missing_optional": [],
            "score": 100
        }
        
        # Check required fields
        for field in required_fields:
            if field not in listing or not listing[field]:
                completeness["missing_required"].append(field)
                completeness["complete"] = False
                completeness["score"] -= 30
                
        # Check optional fields
        for field in optional_fields:
            if field not in listing or not listing[field]:
                completeness["missing_optional"].append(field)
                completeness["score"] -= 10
                
        completeness["score"] = max(0, completeness["score"])
        
        return completeness
        
    def generate_listing_report(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive listing analysis report.
        
        Args:
            listing: Complete listing data
            
        Returns:
            Detailed report
        """
        report = {
            "timestamp": "2025-01-01T00:00:00",
            "overall_score": 0,
            "title_validation": {},
            "bullet_points_validation": {},
            "description_validation": {},
            "completeness": {},
            "recommendations": []
        }
        
        # Validate components
        if "title" in listing and listing["title"]:
            report["title_validation"] = self.validate_title(listing["title"])
            
        if "bullet_points" in listing and listing["bullet_points"]:
            report["bullet_points_validation"] = self.validate_bullet_points(listing["bullet_points"])
            
        if "description" in listing and listing["description"]:
            report["description_validation"] = self.validate_description(listing["description"])
            
        report["completeness"] = self.analyze_listing_completeness(listing)
        
        # Calculate overall score
        scores = [
            report.get("title_validation", {}).get("score", 0),
            report.get("bullet_points_validation", {}).get("score", 0),
            report.get("description_validation", {}).get("score", 0),
            report.get("completeness", {}).get("score", 0)
        ]
        report["overall_score"] = sum(scores) / len(scores) if scores else 0
        
        # Generate recommendations
        if report["overall_score"] < 70:
            report["recommendations"].append("Listing needs improvement")
        if report.get("completeness", {}).get("score", 100) < 100:
            report["recommendations"].append("Complete all required fields")
            
        return report
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "amazon_listing_parser",
            "description": "Parse and validate Amazon product listings. Checks compliance with Amazon's guidelines and character limits.",
            "parameters": {
                "listing_text": {
                    "type": "string",
                    "description": "Amazon listing text to parse and validate"
                }
            }
        }
