"""
Quality Validator Agent - Compliance and Quality Assurance Specialist

This agent validates all content for compliance, accuracy, and quality before deployment.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.logger import Logger
from shared.context_manager import ContextManager
from shared.hallucination_guard import HallucinationGuard
from tools.compliance_checker import ComplianceChecker
from tools.web_search_tool import WebSearchTool


class QualityValidatorAgent:
    """
    Quality Validator Agent - Compliance and quality assurance specialist
    
    Responsibilities:
    - Validate Amazon TOS compliance
    - Detect hallucinations and false claims
    - Verify factual accuracy
    - Check content quality
    - Provide improvement recommendations
    """
    
    def __init__(
        self,
        agent_id: str = "quality_validator",
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the Quality Validator Agent."""
        self.agent_id = agent_id
        self.config = self._load_config(config_path)
        self.memory = memory_manager or MemoryManager()
        self.context = context_manager or ContextManager()
        self.logger = logger or Logger()
        
        # Initialize tools
        self.compliance_checker = ComplianceChecker()
        self.hallucination_guard = HallucinationGuard()
        self.web_search = WebSearchTool()
        
        # Load prompts and tools mapping
        self.prompts = self._load_prompts()
        self.tools_map = self._load_tools_map()
        
        # Agent metadata
        self.role = self.config.get("role", "Quality Validator")
        self.goal = self.config.get("goal", "Ensure compliance and quality")
        self.backstory = self.config.get("backstory", "Expert quality assurance specialist")
        
        self.logger.info(f"Initialized {self.role}", agent_id=self.agent_id)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load agent configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates."""
        prompts_dir = Path(__file__).parent / "prompts"
        prompts = {}
        
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.txt"):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompts[prompt_file.stem] = f.read()
        
        return prompts
    
    def _load_tools_map(self) -> Dict[str, Any]:
        """Load tools mapping."""
        tools_map_path = Path(__file__).parent / "tools_map.yaml"
        
        try:
            with open(tools_map_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}
    
    def validate_campaign(self) -> Dict[str, Any]:
        """
        Validate complete campaign for compliance and quality.
        
        Returns:
            Comprehensive validation report
        """
        self.logger.info("Starting campaign validation", agent_id=self.agent_id)
        
        # Retrieve all content from memory
        listing = self.memory.retrieve(
            agent_id="copywriter",
            key="amazon_listing",
            memory_type="long_term"
        ) or {}
        
        social_campaigns = self.memory.retrieve(
            agent_id="social_media_marketer",
            key="social_campaigns",
            memory_type="long_term"
        ) or {}
        
        market_analysis = self.memory.retrieve(
            agent_id="market_research_analyst",
            key="market_analysis",
            memory_type="long_term"
        ) or {}
        
        # Perform validations
        listing_validation = self.validate_listing(listing)
        social_validation = self.validate_social_content(social_campaigns)
        hallucination_check = self.check_hallucinations(listing, market_analysis)
        compliance_check = self.check_compliance(listing)
        
        # Calculate overall scores
        overall_score = self._calculate_overall_score([
            listing_validation,
            social_validation,
            hallucination_check,
            compliance_check
        ])
        
        validation_report = {
            "overall_score": overall_score,
            "status": self._determine_status(overall_score),
            "listing_validation": listing_validation,
            "social_validation": social_validation,
            "hallucination_check": hallucination_check,
            "compliance_check": compliance_check,
            "recommendations": self._generate_recommendations(
                listing_validation,
                social_validation,
                hallucination_check,
                compliance_check
            ),
            "approval": overall_score >= 75,
            "requires_revision": overall_score < 75
        }
        
        # Store in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="validation_report",
            value=validation_report,
            memory_type="long_term"
        )
        
        # Share with other agents
        self.memory.share_memory(
            source_agent=self.agent_id,
            target_agent="all",
            key="quality_validation",
            value=validation_report
        )
        
        if validation_report["approval"]:
            self.logger.success(f"Campaign approved! Score: {overall_score}/100", agent_id=self.agent_id)
        else:
            self.logger.warning(f"Campaign needs revision. Score: {overall_score}/100", agent_id=self.agent_id)
        
        return validation_report
    
    def validate_listing(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate Amazon listing content.
        
        Args:
            listing: Listing content to validate
            
        Returns:
            Listing validation results
        """
        self.logger.info("Validating listing content", agent_id=self.agent_id)
        
        if not listing:
            return {"score": 0, "issues": ["No listing content found"]}
        
        title = listing.get("title", "")
        bullets = listing.get("bullet_points", [])
        description = listing.get("description", "")
        
        issues = []
        passed_checks = []
        
        # Title validation
        if len(title) < 50:
            issues.append("Title too short (minimum 50 characters recommended)")
        elif len(title) > 200:
            issues.append("Title exceeds 200 character limit")
        else:
            passed_checks.append("Title length appropriate")
        
        # Bullet points validation
        if len(bullets) < 5:
            issues.append(f"Only {len(bullets)} bullet points (5 recommended)")
        else:
            passed_checks.append("All 5 bullet points provided")
        
        for i, bullet in enumerate(bullets):
            if len(bullet) > 500:
                issues.append(f"Bullet {i+1} exceeds 500 characters")
            if len(bullet) < 100:
                issues.append(f"Bullet {i+1} too short (minimum 100 characters recommended)")
        
        # Description validation
        if len(description) < 500:
            issues.append("Description too short (minimum 500 characters recommended)")
        elif len(description) > 2000:
            issues.append("Description very long (may affect readability)")
        else:
            passed_checks.append("Description length appropriate")
        
        # Check for HTML in description
        if "<" in description and ">" in description:
            passed_checks.append("HTML formatting used in description")
        
        # Content quality checks
        if title and title.isupper():
            issues.append("Title is all caps (not recommended)")
        
        score = max(0, 100 - (len(issues) * 10))
        
        return {
            "score": score,
            "passed_checks": passed_checks,
            "issues": issues,
            "status": "Pass" if score >= 75 else "Needs Improvement"
        }
    
    def validate_social_content(self, social_campaigns: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate social media campaign content.
        
        Args:
            social_campaigns: Social media campaigns to validate
            
        Returns:
            Social content validation results
        """
        self.logger.info("Validating social media content", agent_id=self.agent_id)
        
        if not social_campaigns:
            return {"score": 0, "issues": ["No social media campaigns found"]}
        
        issues = []
        passed_checks = []
        
        # Check platform coverage
        required_platforms = ["facebook_campaign", "instagram_campaign", "tiktok_campaign", "pinterest_campaign"]
        for platform in required_platforms:
            if platform in social_campaigns:
                passed_checks.append(f"{platform.replace('_', ' ').title()} strategy provided")
            else:
                issues.append(f"Missing {platform.replace('_', ' ')} strategy")
        
        # Check content calendar
        if "content_calendar" in social_campaigns:
            passed_checks.append("Content calendar included")
        else:
            issues.append("Missing content calendar")
        
        # Check budget allocation
        if "budget_allocation" in social_campaigns:
            passed_checks.append("Budget allocation defined")
        else:
            issues.append("Missing budget allocation")
        
        # Check KPIs
        if "kpis" in social_campaigns:
            passed_checks.append("KPIs defined")
        else:
            issues.append("Missing KPI definitions")
        
        score = max(0, 100 - (len(issues) * 15))
        
        return {
            "score": score,
            "passed_checks": passed_checks,
            "issues": issues,
            "status": "Pass" if score >= 75 else "Needs Improvement"
        }
    
    def check_hallucinations(
        self, 
        listing: Dict[str, Any], 
        market_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check for hallucinations and false claims.
        
        Args:
            listing: Listing content
            market_analysis: Market research data
            
        Returns:
            Hallucination check results
        """
        self.logger.info("Checking for hallucinations", agent_id=self.agent_id)
        
        content_to_check = {
            "title": listing.get("title", ""),
            "bullets": " ".join(listing.get("bullet_points", [])),
            "description": listing.get("description", "")
        }
        
        # Use hallucination guard (correct signature - returns tuple)
        is_valid, validation_result = self.hallucination_guard.validate_content(
            content=content_to_check,
            context={"market_data": market_analysis}
        )
        
        # Check for specific problematic claims
        problematic_phrases = [
            "#1 bestseller",
            "cure",
            "guaranteed to",
            "miracle",
            "FDA approved",
            "scientifically proven"
        ]
        
        found_issues = []
        full_content = str(content_to_check).lower()
        
        for phrase in problematic_phrases:
            if phrase in full_content:
                found_issues.append(f"Potentially problematic claim: '{phrase}'")
        
        validation_result["found_issues"] = found_issues
        validation_result["score"] = max(0, validation_result.get("score", 80) - (len(found_issues) * 10))
        validation_result["is_valid"] = is_valid and len(found_issues) == 0
        
        return validation_result
    
    def check_compliance(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check Amazon TOS compliance.
        
        Args:
            listing: Listing content to check
            
        Returns:
            Compliance check results
        """
        self.logger.info("Checking Amazon TOS compliance", agent_id=self.agent_id)
        
        title = listing.get("title", "")
        bullets = listing.get("bullet_points", [])
        description = listing.get("description", "")
        
        # Combine all content
        all_content = f"{title} {' '.join(bullets)} {description}"
        
        # Use compliance checker
        compliance_result = self.compliance_checker.check_compliance(all_content)
        
        # Additional specific checks
        additional_checks = self._perform_additional_compliance_checks(listing)
        
        compliance_result["additional_checks"] = additional_checks
        
        # Recalculate score
        if additional_checks["issues"]:
            compliance_result["score"] = max(
                0, 
                compliance_result.get("score", 80) - (len(additional_checks["issues"]) * 5)
            )
        
        return compliance_result
    
    def _perform_additional_compliance_checks(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """Perform additional compliance checks."""
        issues = []
        passed = []
        
        title = listing.get("title", "")
        
        # Check for promotional language in title
        promo_words = ["sale", "discount", "free shipping", "limited time", "offer"]
        for word in promo_words:
            if word in title.lower():
                issues.append(f"Promotional language in title: '{word}'")
        
        if not issues:
            passed.append("No promotional language in title")
        
        # Check for seller-specific information
        seller_words = ["we", "our company", "our store"]
        for word in seller_words:
            if word in title.lower():
                issues.append(f"Seller-specific language in title: '{word}'")
        
        if not issues or len(issues) < 2:
            passed.append("Minimal seller-specific language")
        
        return {
            "issues": issues,
            "passed": passed
        }
    
    def _calculate_overall_score(self, validations: List[Dict[str, Any]]) -> int:
        """Calculate overall validation score."""
        scores = [v.get("score", 0) for v in validations if v and "score" in v]
        
        if not scores:
            return 0
        
        return int(sum(scores) / len(scores))
    
    def _determine_status(self, score: int) -> str:
        """Determine campaign status based on score."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Acceptable"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Major Revisions Required"
    
    def _generate_recommendations(
        self,
        listing_validation: Dict[str, Any],
        social_validation: Dict[str, Any],
        hallucination_check: Dict[str, Any],
        compliance_check: Dict[str, Any]
    ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Listing recommendations
        if listing_validation.get("score", 0) < 80:
            for issue in listing_validation.get("issues", []):
                recommendations.append(f"Listing: {issue}")
        
        # Social recommendations
        if social_validation.get("score", 0) < 80:
            for issue in social_validation.get("issues", []):
                recommendations.append(f"Social Media: {issue}")
        
        # Hallucination recommendations
        if hallucination_check.get("score", 0) < 80:
            recommendations.append("Review content for unsupported claims")
            for issue in hallucination_check.get("found_issues", []):
                recommendations.append(f"Content: {issue}")
        
        # Compliance recommendations
        if compliance_check.get("score", 0) < 80:
            for violation in compliance_check.get("violations", []):
                recommendations.append(f"Compliance: {violation}")
        
        if not recommendations:
            recommendations.append("Campaign meets all quality standards!")
        
        return recommendations
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "active",
            "tools_available": ["compliance_checker", "hallucination_guard", "web_search"],
            "memory_keys": list(self.memory.retrieve(self.agent_id, "all", "short_term").keys())
        }
