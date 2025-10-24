"""
Hallucination Guard for ADK Multi-Agent System
Implements multi-layer hallucination detection and mitigation strategies.
"""

from typing import Any, Dict, List, Optional, Tuple
import re
import yaml
from datetime import datetime


class HallucinationGuard:
    """
    Implements hallucination detection and mitigation strategies.
    Uses multiple validation techniques to ensure content accuracy.
    """
    
    def __init__(self, config_path: str = "./config/validator_rules.yaml"):
        """
        Initialize hallucination guard.
        
        Args:
            config_path: Path to validator rules configuration
        """
        self.config = self._load_config(config_path)
        self.validation_results: List[Dict] = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load validation configuration."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load validator config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict:
        """Get default validation configuration."""
        return {
            "validation": {
                "hallucination_detection": {
                    "enabled": True,
                    "factual_consistency": {"enabled": True},
                    "self_consistency": {"enabled": True},
                    "source_grounding": {"enabled": True}
                }
            }
        }
        
    def validate_content(self, content: Dict[str, Any], context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate content for hallucinations and inconsistencies.
        
        Args:
            content: Content to validate
            context: Context information (product info, sources, etc.)
            
        Returns:
            Tuple of (is_valid, validation_report)
        """
        validation_report = {
            "timestamp": datetime.now().isoformat(),
            "checks_performed": [],
            "violations": [],
            "warnings": [],
            "score": 100
        }
        
        config = self.config.get("validation", {}).get("hallucination_detection", {})
        
        if not config.get("enabled", True):
            return True, validation_report
            
        # Factual consistency checks
        if config.get("factual_consistency", {}).get("enabled", True):
            self._check_factual_consistency(content, context, validation_report)
            
        # Self-consistency checks
        if config.get("self_consistency", {}).get("enabled", True):
            self._check_self_consistency(content, validation_report)
            
        # Source grounding checks
        if config.get("source_grounding", {}).get("enabled", True):
            self._check_source_grounding(content, context, validation_report)
            
        # Calculate final score
        violation_penalties = {
            "critical": 50,
            "high": 30,
            "medium": 15,
            "low": 5
        }
        
        for violation in validation_report["violations"]:
            penalty = violation_penalties.get(violation.get("severity", "low"), 5)
            validation_report["score"] -= penalty
            
        validation_report["score"] = max(0, validation_report["score"])
        
        is_valid = validation_report["score"] >= 50  # Threshold for validity
        
        return is_valid, validation_report
        
    def _check_factual_consistency(self, content: Dict, context: Dict, report: Dict):
        """Check factual consistency across content."""
        report["checks_performed"].append("factual_consistency")
        
        # Check product attributes consistency
        if "product_info" in context and isinstance(content, dict):
            product_info = context["product_info"]
            
            # Check if product name is consistent
            if "product_name" in product_info:
                expected_name = product_info["product_name"]
                content_str = str(content).lower()
                
                # Look for variations or inconsistencies
                if expected_name.lower() not in content_str:
                    report["warnings"].append({
                        "type": "product_name_inconsistency",
                        "message": f"Product name '{expected_name}' not found in content",
                        "severity": "medium"
                    })
                    
        # Check numerical consistency
        self._check_numerical_consistency(content, report)
        
    def _check_numerical_consistency(self, content: Dict, report: Dict):
        """Check numerical values for consistency."""
        content_str = str(content)
        
        # Find all numbers in content
        numbers = re.findall(r'\d+(?:\.\d+)?', content_str)
        
        # Check for suspiciously large or unrealistic numbers
        for num_str in numbers:
            num = float(num_str)
            
            # Flag suspiciously large percentages
            if "%" in content_str or "percent" in content_str.lower():
                if num > 100:
                    report["violations"].append({
                        "type": "unrealistic_percentage",
                        "message": f"Percentage value {num}% exceeds 100%",
                        "severity": "high"
                    })
                    
    def _check_self_consistency(self, content: Dict, report: Dict):
        """Check for internal contradictions."""
        report["checks_performed"].append("self_consistency")
        
        if not isinstance(content, dict):
            return
            
        # Check for contradictory claims
        content_str = str(content).lower()
        
        # Common contradictions
        contradictions = [
            (["best", "top", "#1"], ["average", "standard"]),
            (["always", "100%"], ["sometimes", "may"]),
            (["guaranteed"], ["might", "could"]),
            (["free"], ["cost", "price", "$"])
        ]
        
        for positive_terms, negative_terms in contradictions:
            has_positive = any(term in content_str for term in positive_terms)
            has_negative = any(term in content_str for term in negative_terms)
            
            if has_positive and has_negative:
                report["warnings"].append({
                    "type": "potential_contradiction",
                    "message": f"Content contains potentially contradictory claims",
                    "severity": "medium"
                })
                
    def _check_source_grounding(self, content: Dict, context: Dict, report: Dict):
        """Check if content is grounded in provided sources."""
        report["checks_performed"].append("source_grounding")
        
        # Check for unsubstantiated superlatives
        content_str = str(content).lower()
        
        unsubstantiated_claims = [
            "best in the world",
            "number one",
            "only product",
            "guaranteed to cure",
            "clinically proven",
            "fda approved"
        ]
        
        for claim in unsubstantiated_claims:
            if claim in content_str:
                # Check if there's supporting evidence in context
                has_evidence = False
                if "market_insights" in context:
                    insights_str = str(context["market_insights"]).lower()
                    has_evidence = claim in insights_str
                    
                if not has_evidence:
                    report["violations"].append({
                        "type": "unsubstantiated_claim",
                        "message": f"Claim '{claim}' lacks supporting evidence",
                        "severity": "high"
                    })
                    
    def check_attribute_consistency(self, content: Dict, reference: Dict) -> bool:
        """
        Check if attributes in content match reference.
        
        Args:
            content: Generated content
            reference: Reference data (product info, etc.)
            
        Returns:
            True if consistent
        """
        if not isinstance(content, dict) or not isinstance(reference, dict):
            return True
            
        # Check key attributes
        key_attributes = ["product_name", "brand_name", "category"]
        
        for attr in key_attributes:
            if attr in reference and attr in content:
                if content[attr].lower() != reference[attr].lower():
                    return False
                    
        return True
        
    def detect_fabricated_features(self, features: List[str], known_features: List[str]) -> List[str]:
        """
        Detect potentially fabricated features.
        
        Args:
            features: Generated features
            known_features: Known valid features
            
        Returns:
            List of suspicious features
        """
        suspicious = []
        
        for feature in features:
            # Check if feature is too generic or vague
            vague_terms = ["high quality", "best", "premium", "luxury", "amazing"]
            if any(term in feature.lower() for term in vague_terms) and len(feature.split()) < 5:
                suspicious.append(feature)
                
            # Check if feature contains specific claims without context
            specific_claims = ["fastest", "strongest", "most durable", "longest lasting"]
            if any(claim in feature.lower() for claim in specific_claims):
                # Should have supporting details
                if len(feature.split()) < 8:
                    suspicious.append(feature)
                    
        return suspicious
        
    def validate_statistics(self, content: str) -> List[Dict[str, Any]]:
        """
        Validate statistical claims in content.
        
        Args:
            content: Content containing statistics
            
        Returns:
            List of validation issues
        """
        issues = []
        
        # Find percentage claims
        percentage_pattern = r'(\d+(?:\.\d+)?)\s*%'
        percentages = re.finditer(percentage_pattern, content)
        
        for match in percentages:
            value = float(match.group(1))
            
            # Check for unrealistic percentages
            if value > 100:
                issues.append({
                    "type": "invalid_percentage",
                    "value": value,
                    "message": f"Percentage {value}% exceeds 100%"
                })
            elif value == 100 and "up to" not in content.lower():
                issues.append({
                    "type": "absolute_claim",
                    "value": value,
                    "message": "100% claim without qualifier"
                })
                
        return issues
        
    def check_temporal_consistency(self, content: str) -> bool:
        """
        Check temporal references for consistency.
        
        Args:
            content: Content to check
            
        Returns:
            True if temporally consistent
        """
        # Find year references
        years = re.findall(r'\b(19|20)\d{2}\b', content)
        current_year = datetime.now().year
        
        for year_str in years:
            year = int(year_str)
            
            # Flag future years
            if year > current_year:
                return False
                
            # Flag very old years in "new" products
            if "new" in content.lower() and year < current_year - 2:
                return False
                
        return True
        
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of all validations performed.
        
        Returns:
            Validation summary
        """
        return {
            "total_validations": len(self.validation_results),
            "passed": sum(1 for v in self.validation_results if v.get("score", 0) >= 75),
            "failed": sum(1 for v in self.validation_results if v.get("score", 0) < 50),
            "warnings": sum(1 for v in self.validation_results if 50 <= v.get("score", 0) < 75),
            "recent_validations": self.validation_results[-5:] if self.validation_results else []
        }
