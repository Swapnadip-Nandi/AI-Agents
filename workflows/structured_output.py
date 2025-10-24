"""
Structured Output Generator - Create JSON and Markdown Reports

Generates structured campaign outputs in multiple formats.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.logger import Logger


class StructuredOutputGenerator:
    """Generate structured outputs in JSON and Markdown formats."""
    
    def __init__(
        self,
        memory_manager: MemoryManager,
        logger: Logger,
        output_dir: str = "./storage/results"
    ):
        """Initialize output generator."""
        self.memory = memory_manager
        self.logger = logger
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_outputs(self, campaign_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate both JSON and Markdown outputs.
        
        Args:
            campaign_results: Complete campaign results
            
        Returns:
            Dictionary with paths to generated files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate JSON output
        json_path = self.output_dir / f"campaign_{timestamp}.json"
        self._generate_json(campaign_results, json_path)
        
        # Generate Markdown report
        md_path = self.output_dir / f"campaign_{timestamp}.md"
        self._generate_markdown(campaign_results, md_path)
        
        self.logger.success(f"Generated outputs: {json_path.name}, {md_path.name}")
        
        return {
            "json": str(json_path),
            "markdown": str(md_path)
        }
    
    def _generate_json(self, data: Dict[str, Any], output_path: Path):
        """Generate JSON output."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"JSON output saved: {output_path}")
    
    def _generate_markdown(self, data: Dict[str, Any], output_path: Path):
        """Generate Markdown report."""
        md_content = self._format_markdown(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        self.logger.info(f"Markdown report saved: {output_path}")
    
    def _format_markdown(self, data: Dict[str, Any]) -> str:
        """Format data as Markdown report."""
        product_name = data.get("product_info", {}).get("name", "Unknown Product")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        validation = data.get("validation_report", {})
        listing = data.get("amazon_listing", {})
        social = data.get("social_campaigns", {})
        metrics = data.get("workflow_metrics", {})
        
        md = f"""# Amazon Campaign Report: {product_name}

**Generated:** {timestamp}

---

## Executive Summary

- **Overall Quality Score:** {validation.get('overall_score', 'N/A')}/100
- **Campaign Status:** {validation.get('status', 'Unknown')}
- **Approval Status:** {'✅ APPROVED' if validation.get('approval') else '⚠️ NEEDS REVISION'}
- **Workflow Duration:** {metrics.get('total_duration', 'N/A')} seconds

---

## 1. Strategic Plan

{self._format_strategic_plan(data.get('strategic_plan', {}))}

---

## 2. Market Analysis

{self._format_market_analysis(data.get('market_analysis', {}))}

---

## 3. SEO Strategy

{self._format_seo_strategy(data.get('keyword_research', {}))}

---

## 4. Amazon Listing

### Title
```
{listing.get('title', 'N/A')}
```

### Bullet Points
{self._format_bullets(listing.get('bullet_points', []))}

### Description
{listing.get('description', 'N/A')}

### Validation Scores
- **Title:** {listing.get('title_validation', {}).get('score', 'N/A')}/100
- **Bullets:** {listing.get('bullets_validation', {}).get('score', 'N/A')}/100
- **Description:** {listing.get('description_validation', {}).get('score', 'N/A')}/100
- **Overall:** {listing.get('overall_score', 'N/A')}/100

---

## 5. Social Media Campaigns

{self._format_social_campaigns(social)}

---

## 6. Quality Validation Report

### Overall Assessment
- **Score:** {validation.get('overall_score', 'N/A')}/100
- **Status:** {validation.get('status', 'Unknown')}
- **Approved:** {'Yes' if validation.get('approval') else 'No'}

### Validation Details
{self._format_validation_details(validation)}

### Recommendations
{self._format_recommendations(validation.get('recommendations', []))}

---

## 7. Workflow Metrics

{self._format_workflow_metrics(metrics)}

---

## Next Steps

{self._format_next_steps(validation)}

---

**Report End**
"""
        return md
    
    def _format_strategic_plan(self, plan: Dict[str, Any]) -> str:
        """Format strategic plan section."""
        if not plan:
            return "No strategic plan available."
        
        objectives = plan.get('objectives', [])
        timeline = plan.get('timeline', {})
        
        md = f"### Campaign Objectives\n\n"
        for i, obj in enumerate(objectives, 1):
            md += f"{i}. {obj}\n"
        
        md += f"\n### Timeline\n\n"
        for phase, duration in timeline.items():
            md += f"- **{phase.replace('_', ' ').title()}:** {duration}\n"
        
        return md
    
    def _format_market_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format market analysis section."""
        if not analysis:
            return "No market analysis available."
        
        return f"""### Market Overview
- **Market Size:** {analysis.get('market_size', 'N/A')}
- **Growth Rate:** {analysis.get('growth_rate', 'N/A')}
- **Price Sensitivity:** {analysis.get('price_sensitivity', 'N/A')}

### Key Trends
{self._format_list(analysis.get('trends', []))}

### Opportunities
{self._format_list(analysis.get('opportunities', []))}
"""
    
    def _format_seo_strategy(self, keywords: Dict[str, Any]) -> str:
        """Format SEO strategy section."""
        if not keywords:
            return "No SEO strategy available."
        
        primary = keywords.get('primary_keywords', [])
        
        md = "### Primary Keywords\n\n"
        for kw in primary[:5]:
            if isinstance(kw, dict):
                md += f"- **{kw.get('keyword')}**: Volume: {kw.get('search_volume', 'N/A')}, "
                md += f"Competition: {kw.get('competition', 'N/A')}\n"
        
        return md
    
    def _format_bullets(self, bullets: list) -> str:
        """Format bullet points."""
        if not bullets:
            return "No bullet points available."
        
        md = ""
        for i, bullet in enumerate(bullets, 1):
            md += f"\n**{i}.** {bullet}\n"
        
        return md
    
    def _format_social_campaigns(self, social: Dict[str, Any]) -> str:
        """Format social campaigns section."""
        if not social:
            return "No social campaigns available."
        
        platforms = ['facebook_campaign', 'instagram_campaign', 'tiktok_campaign', 'pinterest_campaign']
        
        md = ""
        for platform in platforms:
            if platform in social:
                platform_name = platform.replace('_campaign', '').title()
                md += f"\n### {platform_name}\n"
                md += f"- Campaign strategy defined ✓\n"
        
        budget = social.get('budget_allocation', {})
        if budget:
            md += f"\n### Budget Allocation\n"
            md += f"- **Total Monthly Budget:** {budget.get('total_monthly', 'N/A')}\n"
        
        return md
    
    def _format_validation_details(self, validation: Dict[str, Any]) -> str:
        """Format validation details."""
        components = {
            'listing_validation': 'Listing Content',
            'social_validation': 'Social Media Content',
            'hallucination_check': 'Factual Accuracy',
            'compliance_check': 'Amazon Compliance'
        }
        
        md = ""
        for key, name in components.items():
            if key in validation:
                score = validation[key].get('score', 'N/A')
                status = validation[key].get('status', 'Unknown')
                md += f"- **{name}:** {score}/100 ({status})\n"
        
        return md
    
    def _format_recommendations(self, recommendations: list) -> str:
        """Format recommendations."""
        if not recommendations:
            return "No recommendations - all quality standards met!"
        
        md = ""
        for i, rec in enumerate(recommendations, 1):
            md += f"{i}. {rec}\n"
        
        return md
    
    def _format_workflow_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format workflow metrics."""
        if not metrics:
            return "No metrics available."
        
        return f"""- **Total Duration:** {metrics.get('total_duration', 'N/A')} seconds
- **Agents Executed:** {metrics.get('agents_executed', 'N/A')}
- **Stages Completed:** {metrics.get('stages_completed', 'N/A')}
- **Success Rate:** {metrics.get('success_rate', 'N/A')}%
"""
    
    def _format_next_steps(self, validation: Dict[str, Any]) -> str:
        """Format next steps."""
        if validation.get('approval'):
            return """1. Deploy campaign to Amazon
2. Launch social media campaigns
3. Monitor performance metrics
4. Optimize based on results
"""
        else:
            return """1. Review validation feedback
2. Make recommended revisions
3. Resubmit for validation
4. Deploy after approval
"""
    
    def _format_list(self, items: list) -> str:
        """Format a list of items."""
        if not items:
            return "N/A"
        
        return "\n".join([f"- {item}" for item in items])
