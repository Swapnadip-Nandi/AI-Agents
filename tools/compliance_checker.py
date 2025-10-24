"""
Compliance Checker (Custom Tool)
Validates content against Amazon TOS and marketplace policies.
"""

from typing import Any, Dict, List, Optional
import re
import yaml


class ComplianceChecker:
    """
    Custom compliance checking tool for Amazon marketplace policies.
    """
    
    def __init__(self, rules_config_path: str = "./config/validator_rules.yaml"):
        """
        Initialize compliance checker.
        
        Args:
            rules_config_path: Path to validation rules configuration
        """
        self.rules = self._load_rules(rules_config_path)
        self.violation_history: List[Dict] = []
        
    def _load_rules(self, config_path: str) -> Dict:
        """Load compliance rules from configuration."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("validation", {}).get("amazon_compliance", {})
        except Exception as e:
            print(f"Warning: Could not load compliance rules: {e}")
            return self._get_default_rules()
            
    def _get_default_rules(self) -> Dict:
        """Get default compliance rules."""
        return {
            "content_policy": {
                "enabled": True,
                "prohibited_content": [
                    {
                        "category": "medical_claims",
                        "severity": "critical",
                        "patterns": ["cure", "treat disease", "clinically proven"]
                    }
                ]
            }
        }
        
    def check_compliance(self, content: str, content_type: str = "general") -> Dict[str, Any]:
        """
        Check content for compliance violations.
        
        Args:
            content: Content to check
            content_type: Type of content (title, bullet_points, description, etc.)
            
        Returns:
            Compliance check result
        """
        result = {
            "compliant": True,
            "violations": [],
            "warnings": [],
            "score": 100,
            "content_type": content_type
        }
        
        # Check prohibited content
        self._check_prohibited_content(content, result)
        
        # Check character limits
        self._check_character_limits(content, content_type, result)
        
        # Check prohibited keywords
        self._check_prohibited_keywords(content, result)
        
        # Calculate compliance score
        critical_count = sum(1 for v in result["violations"] if v.get("severity") == "critical")
        high_count = sum(1 for v in result["violations"] if v.get("severity") == "high")
        medium_count = sum(1 for v in result["violations"] if v.get("severity") == "medium")
        
        result["score"] -= (critical_count * 50 + high_count * 25 + medium_count * 10)
        result["score"] = max(0, result["score"])
        result["compliant"] = result["score"] >= 70
        
        # Log violation
        if not result["compliant"]:
            self.violation_history.append({
                "content_type": content_type,
                "violations": len(result["violations"]),
                "score": result["score"]
            })
            
        return result
        
    def _check_prohibited_content(self, content: str, result: Dict):
        """Check for prohibited content patterns."""
        content_policy = self.rules.get("content_policy", {})
        if not content_policy.get("enabled", True):
            return
            
        prohibited_list = content_policy.get("prohibited_content", [])
        content_lower = content.lower()
        
        for category in prohibited_list:
            patterns = category.get("patterns", [])
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    result["violations"].append({
                        "type": category["category"],
                        "severity": category["severity"],
                        "pattern": pattern,
                        "message": f"Prohibited content detected: {pattern}"
                    })
                    result["compliant"] = False
                    
    def _check_character_limits(self, content: str, content_type: str, result: Dict):
        """Check character limits."""
        limits = {
            "title": 200,
            "bullet_point": 500,
            "description": 2000,
            "search_terms": 250
        }
        
        if content_type in limits:
            max_chars = limits[content_type]
            if len(content) > max_chars:
                result["violations"].append({
                    "type": "character_limit_exceeded",
                    "severity": "high",
                    "message": f"{content_type} exceeds {max_chars} characters (current: {len(content)})"
                })
                result["compliant"] = False
                
    def _check_prohibited_keywords(self, content: str, result: Dict):
        """Check for prohibited keywords."""
        keyword_restrictions = self.rules.get("keyword_restrictions", {})
        if not keyword_restrictions.get("enabled", True):
            return
            
        prohibited_keywords = keyword_restrictions.get("prohibited_keywords", [])
        content_lower = content.lower()
        
        for keyword in prohibited_keywords:
            if keyword.lower() in content_lower:
                result["violations"].append({
                    "type": "prohibited_keyword",
                    "severity": "high",
                    "keyword": keyword,
                    "message": f"Prohibited keyword: {keyword}"
                })
                result["compliant"] = False
                
    def check_listing_compliance(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check complete listing for compliance.
        
        Args:
            listing: Complete listing data
            
        Returns:
            Comprehensive compliance report
        """
        report = {
            "overall_compliant": True,
            "overall_score": 100,
            "component_results": {}
        }
        
        # Check each component
        if "title" in listing:
            report["component_results"]["title"] = self.check_compliance(listing["title"], "title")
            
        if "bullet_points" in listing:
            for i, bullet in enumerate(listing["bullet_points"]):
                key = f"bullet_point_{i+1}"
                report["component_results"][key] = self.check_compliance(bullet, "bullet_point")
                
        if "description" in listing:
            report["component_results"]["description"] = self.check_compliance(listing["description"], "description")
            
        # Calculate overall score
        scores = [r["score"] for r in report["component_results"].values()]
        report["overall_score"] = sum(scores) / len(scores) if scores else 100
        report["overall_compliant"] = report["overall_score"] >= 70
        
        return report
        
    def check_brand_safety(self, content: str, brand_name: str) -> Dict[str, Any]:
        """
        Check brand safety compliance.
        
        Args:
            content: Content to check
            brand_name: Brand name to verify
            
        Returns:
            Brand safety check result
        """
        result = {
            "safe": True,
            "issues": [],
            "score": 100
        }
        
        content_lower = content.lower()
        brand_lower = brand_name.lower()
        
        # Check if brand name is present
        if brand_lower not in content_lower:
            result["issues"].append({
                "type": "missing_brand_name",
                "severity": "medium",
                "message": "Brand name not mentioned in content"
            })
            result["score"] -= 20
            
        # Check for competitor mentions
        competitor_indicators = ["vs", "versus", "compared to", "better than"]
        if any(ind in content_lower for ind in competitor_indicators):
            result["issues"].append({
                "type": "competitor_mention",
                "severity": "medium",
                "message": "Content may contain competitor comparisons"
            })
            result["score"] -= 15
            
        result["safe"] = result["score"] >= 70
        
        return result
        
    def validate_claims(self, claims: List[str]) -> Dict[str, Any]:
        """
        Validate product claims for compliance.
        
        Args:
            claims: List of product claims
            
        Returns:
            Claims validation result
        """
        result = {
            "valid_claims": [],
            "invalid_claims": [],
            "questionable_claims": [],
            "score": 100
        }
        
        for claim in claims:
            claim_lower = claim.lower()
            
            # Check for absolute claims
            absolute_terms = ["guaranteed", "100%", "always", "never", "best", "only"]
            if any(term in claim_lower for term in absolute_terms):
                result["invalid_claims"].append({
                    "claim": claim,
                    "reason": "Contains absolute term without proof"
                })
                result["score"] -= 20
            # Check for medical/health claims
            elif any(term in claim_lower for term in ["cure", "heal", "treat", "medical"]):
                result["invalid_claims"].append({
                    "claim": claim,
                    "reason": "Contains medical claim"
                })
                result["score"] -= 30
            # Check for vague claims
            elif any(term in claim_lower for term in ["high quality", "premium", "luxury"]) and len(claim.split()) < 5:
                result["questionable_claims"].append({
                    "claim": claim,
                    "reason": "Vague claim without specifics"
                })
                result["score"] -= 10
            else:
                result["valid_claims"].append(claim)
                
        result["score"] = max(0, result["score"])
        
        return result
        
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get compliance check summary."""
        return {
            "total_checks": len(self.violation_history),
            "violations_found": sum(v["violations"] for v in self.violation_history),
            "average_score": sum(v["score"] for v in self.violation_history) / len(self.violation_history) if self.violation_history else 100
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "compliance_checker",
            "description": "Check content for Amazon TOS compliance and marketplace policy violations. Validates against prohibited content, character limits, and brand safety.",
            "parameters": {
                "content": {
                    "type": "string",
                    "description": "Content to check for compliance"
                },
                "content_type": {
                    "type": "string",
                    "description": "Type of content (title, bullet_points, description)",
                    "optional": True
                }
            }
        }
