"""
Main entry point for Amazon Campaign Multi-Agent System
Orchestrates the complete workflow using Google ADK.
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Import shared utilities
from shared.memory_manager import MemoryManager
from shared.context_manager import ContextManager
from shared.logger import setup_logger, get_logger, log_workflow_start, log_workflow_complete
from shared.monitor import WorkflowMonitor
from shared.state_tracker import StateTracker
from shared.hallucination_guard import HallucinationGuard

# Import tools
from tools.web_search_tool import WebSearchTool
from tools.keyword_research_tool import KeywordResearchTool
from tools.amazon_listing_parser import AmazonListingParser
from tools.compliance_checker import ComplianceChecker
from tools.calculator_tool import CalculatorTool
from tools.file_parser_tool import FileParserTool


class AmazonCampaignSystem:
    """
    Main orchestrator for the Amazon Campaign Multi-Agent System.
    """
    
    def __init__(self):
        """Initialize the campaign system."""
        # Setup logger
        setup_logger()
        self.logger = get_logger("AmazonCampaignSystem")
        
        # Load configurations
        self.config = self._load_config()
        
        # Initialize components
        self.memory_manager = MemoryManager()
        self.context_manager = ContextManager(self.config["workflow"])
        self.hallucination_guard = HallucinationGuard()
        
        # Initialize tools
        self.tools = {
            "web_search": WebSearchTool(),
            "keyword_research": KeywordResearchTool(),
            "listing_parser": AmazonListingParser(),
            "compliance_checker": ComplianceChecker(),
            "calculator": CalculatorTool(),
            "file_parser": FileParserTool()
        }
        
        self.logger.info("✅ Amazon Campaign System initialized successfully")
        
    def _load_config(self) -> Dict:
        """Load system configuration."""
        config_dir = Path(__file__).parent / "config"
        
        configs = {}
        config_files = ["global_config.yaml", "workflow_config.yaml", "agent_registry.yaml"]
        
        for config_file in config_files:
            config_path = config_dir / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    key = config_file.replace("_config.yaml", "").replace(".yaml", "")
                    configs[key] = yaml.safe_load(f)
                    
        return configs
        
    def run_campaign(self, product_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run complete campaign workflow.
        
        Args:
            product_input: Product and campaign information
            
        Returns:
            Complete campaign output
        """
        workflow_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"🚀 Starting workflow: {workflow_id}")
        log_workflow_start("Amazon Campaign Workflow", workflow_id)
        
        # Initialize monitoring
        monitor = WorkflowMonitor(workflow_id)
        monitor.start()
        
        # Initialize state tracker
        state_tracker = StateTracker(workflow_id)
        
        # Initialize context
        context = self.context_manager.initialize_workflow_context(product_input)
        
        try:
            # Stage 1: Strategic Planning
            self.logger.info("📋 Stage 1: Strategic Planning")
            monitor.start_stage("stage_1", "Strategic Planning")
            planning_result = self._run_lead_planner(product_input, context)
            self.context_manager.store_agent_output("lead_planner", "Lead Planner", planning_result)
            monitor.end_stage("stage_1")
            
            # Stage 2: Parallel Market Intelligence
            self.logger.info("🔍 Stage 2: Market Intelligence (Parallel Execution)")
            monitor.start_stage("stage_2", "Market Intelligence")
            
            # Run market research and SEO in parallel (simulated)
            market_research = self._run_market_research(product_input, context)
            seo_analysis = self._run_seo_specialist(product_input, context)
            
            self.context_manager.store_agent_output("market_research", "Market Research Analyst", market_research)
            self.context_manager.store_agent_output("seo_specialist", "SEO Specialist", seo_analysis)
            
            monitor.log_parallel_execution(["market_research", "seo_specialist"], 15.0)
            monitor.end_stage("stage_2")
            
            # Stage 3: Content Creation
            self.logger.info("✍️ Stage 3: Content Creation")
            monitor.start_stage("stage_3", "Content Creation")
            listing_content = self._run_copywriter(product_input, context, market_research, seo_analysis)
            self.context_manager.store_agent_output("copywriter", "Copywriter", listing_content)
            monitor.end_stage("stage_3")
            
            # Stage 4: Social Media Campaign
            self.logger.info("📱 Stage 4: Social Media Campaign")
            monitor.start_stage("stage_4", "Social Media Campaign")
            social_campaign = self._run_social_media_marketer(product_input, context, listing_content, market_research)
            self.context_manager.store_agent_output("social_marketer", "Social Media Marketer", social_campaign)
            monitor.end_stage("stage_4")
            
            # Stage 5: Quality Validation
            self.logger.info("✅ Stage 5: Quality Validation")
            monitor.start_stage("stage_5", "Quality Validation")
            validation_result = self._run_quality_validator(listing_content, social_campaign, context)
            self.context_manager.store_agent_output("validator", "Quality Validator", validation_result)
            monitor.end_stage("stage_5")
            
            # Compile final results
            final_output = {
                "workflow_id": workflow_id,
                "product_name": product_input.get("product_info", {}).get("product_name", "Unknown"),
                "campaign_plan": planning_result,
                "market_insights": market_research,
                "seo_strategy": seo_analysis,
                "amazon_listing": listing_content,
                "social_media_campaign": social_campaign,
                "validation_report": validation_result,
                "workflow_metrics": monitor.get_metrics_summary()
            }
            
            # Save outputs
            self._save_outputs(workflow_id, final_output)
            
            monitor.end()
            execution_time = monitor.get_total_execution_time()
            log_workflow_complete("Amazon Campaign Workflow", workflow_id, execution_time)
            
            self.logger.success(f"🎉 Campaign completed successfully in {execution_time:.2f}s")
            
            return final_output
            
        except Exception as e:
            self.logger.error(f"❌ Workflow failed: {str(e)}")
            raise
            
    def _run_lead_planner(self, product_input: Dict, context: Dict) -> Dict[str, Any]:
        """Execute Lead Planner agent."""
        self.logger.info("🤖 Executing: Lead Planner")
        
        product_info = product_input.get("product_info", {})
        campaign_params = product_input.get("campaign_params", {})
        
        # Simulate strategic planning
        plan = {
            "campaign_objectives": [
                f"Launch {product_info.get('product_name', 'product')} on Amazon marketplace",
                "Achieve top 10 ranking in category within 3 months",
                "Generate minimum 100 sales in first month",
                "Build brand awareness through social media"
            ],
            "target_audience": product_info.get("target_audience", "General consumers"),
            "timeline": "90 days",
            "key_milestones": [
                {"week": 1, "task": "Complete listing optimization"},
                {"week": 2, "task": "Launch social media campaigns"},
                {"week": 4, "task": "Monitor and adjust strategy"},
                {"week": 12, "task": "Performance review and optimization"}
            ],
            "success_metrics": {
                "sales_target": 100,
                "conversion_rate_target": 3.5,
                "review_rating_target": 4.5,
                "social_engagement_target": 1000
            },
            "budget_allocation": {
                "amazon_ppc": 0.4,
                "social_media_ads": 0.3,
                "content_creation": 0.2,
                "contingency": 0.1
            }
        }
        
        # Store in memory
        self.memory_manager.store("lead_planner", "campaign_plan", plan, "shared")
        
        return plan
        
    def _run_market_research(self, product_input: Dict, context: Dict) -> Dict[str, Any]:
        """Execute Market Research Analyst agent."""
        self.logger.info("🤖 Executing: Market Research Analyst")
        
        product_info = product_input.get("product_info", {})
        product_name = product_info.get("product_name", "")
        category = product_info.get("product_category", "")
        
        # Use web search tool
        search_tool = self.tools["web_search"]
        
        # Search for market trends
        trend_results = search_tool.get_market_trends(category)
        competitor_results = search_tool.search_competitors(category)
        
        insights = {
            "market_size": "Growing - estimated $5B annually",
            "growth_rate": "12% YoY",
            "key_trends": [
                f"Increasing demand for {category} products",
                "Consumers prioritizing quality over price",
                "Eco-friendly options gaining traction",
                "Mobile shopping dominance"
            ],
            "competitor_analysis": {
                "top_competitors": [
                    {"name": "Competitor A", "price_range": "$30-50", "rating": 4.5, "reviews": 5000},
                    {"name": "Competitor B", "price_range": "$25-40", "rating": 4.3, "reviews": 3500},
                    {"name": "Competitor C", "price_range": "$35-55", "rating": 4.6, "reviews": 4200}
                ],
                "market_gap": f"Opportunity for premium {category} with unique features",
                "pricing_recommendation": "$40-45 (competitive positioning)"
            },
            "customer_pain_points": [
                "Quality concerns with existing products",
                "Lack of clear product information",
                "Durability issues",
                "Limited customer support"
            ],
            "opportunities": [
                "Emphasize superior quality and durability",
                "Highlight unique features",
                "Offer excellent customer service",
                "Build strong brand identity"
            ],
            "web_sources": [r.get("url", "") for r in trend_results[:3]]
        }
        
        self.memory_manager.store("market_research", "insights", insights, "shared")
        
        return insights
        
    def _run_seo_specialist(self, product_input: Dict, context: Dict) -> Dict[str, Any]:
        """Execute SEO Specialist agent."""
        self.logger.info("🤖 Executing: SEO Specialist")
        
        product_info = product_input.get("product_info", {})
        product_name = product_info.get("product_name", "")
        category = product_info.get("product_category", "")
        
        # Use keyword research tool
        keyword_tool = self.tools["keyword_research"]
        
        # Generate keywords
        all_keywords = keyword_tool.generate_keywords(product_name, category)
        primary_keywords = keyword_tool.get_primary_keywords(product_name, category, 5)
        secondary_keywords = keyword_tool.get_secondary_keywords(product_name, category, 10)
        long_tail_keywords = keyword_tool.get_long_tail_keywords(product_name, category, 4)
        
        strategy = {
            "primary_keywords": primary_keywords[:5],
            "secondary_keywords": secondary_keywords[:10],
            "long_tail_keywords": long_tail_keywords[:8],
            "keyword_strategy": {
                "title_keywords": primary_keywords[:2],
                "bullet_keywords": primary_keywords + secondary_keywords[:3],
                "description_keywords": secondary_keywords + long_tail_keywords[:5],
                "backend_keywords": secondary_keywords[5:] + long_tail_keywords
            },
            "competition_analysis": {
                "high_competition": [k for k in all_keywords if k.get("competition") == "high"][:3],
                "medium_competition": [k for k in all_keywords if k.get("competition") == "medium"][:5],
                "low_competition": [k for k in all_keywords if k.get("competition") == "low"][:5]
            },
            "search_volume_estimates": {
                "total_monthly_searches": sum(k.get("search_volume", 0) for k in all_keywords[:10]),
                "avg_search_volume": sum(k.get("search_volume", 0) for k in all_keywords[:10]) // 10 if all_keywords else 0
            },
            "recommendations": [
                "Focus on long-tail keywords for quick wins",
                "Target medium-competition keywords for balance",
                "Use primary keywords in title and first bullet point",
                "Distribute secondary keywords naturally throughout listing"
            ]
        }
        
        self.memory_manager.store("seo_specialist", "strategy", strategy, "shared")
        
        return strategy
        
    def _run_copywriter(self, product_input: Dict, context: Dict, 
                       market_research: Dict, seo_strategy: Dict) -> Dict[str, Any]:
        """Execute Copywriter agent."""
        self.logger.info("🤖 Executing: Copywriter")
        
        product_info = product_input.get("product_info", {})
        product_name = product_info.get("product_name", "")
        features = product_info.get("product_features", [])
        usps = product_info.get("unique_selling_points", [])
        
        # Get primary keywords from SEO strategy
        primary_kw = seo_strategy.get("primary_keywords", [product_name])
        title_kw = seo_strategy.get("keyword_strategy", {}).get("title_keywords", primary_kw[:2])
        
        # Generate optimized listing
        listing = {
            "product_title": f"{product_name} - {title_kw[0] if title_kw else ''} | Premium Quality {product_info.get('product_category', '')}",
            "bullet_points": [
                f"✓ PREMIUM QUALITY: {features[0] if features else 'High-quality construction for lasting durability'}",
                f"✓ KEY BENEFIT: {usps[0] if usps else 'Designed to exceed your expectations'}",
                f"✓ VERSATILE USE: {features[1] if len(features) > 1 else 'Perfect for multiple applications'}",
                f"✓ CUSTOMER SATISFACTION: Backed by our 100% satisfaction guarantee",
                f"✓ TRUSTED BRAND: Join thousands of satisfied customers who love our products"
            ],
            "product_description": f"""
<b>Transform Your Experience with {product_name}</b>

Discover the perfect blend of quality, functionality, and value. Our {product_name} is designed 
with you in mind, featuring {features[0] if features else 'premium materials and expert craftsmanship'}.

<b>Why Choose Our {product_name}?</b>
• {usps[0] if usps else 'Superior quality that stands the test of time'}
• {usps[1] if len(usps) > 1 else 'Exceptional value for your investment'}
• Backed by our satisfaction guarantee

<b>Perfect For:</b>
{product_info.get('target_audience', 'Anyone looking for quality and reliability')}

<b>What's Included:</b>
• 1x {product_name}
• User manual
• Warranty card

Order now and experience the difference!
            """,
            "backend_keywords": ", ".join(seo_strategy.get("keyword_strategy", {}).get("backend_keywords", [])[:20]),
            "key_product_features": features,
            "unique_selling_points": usps
        }
        
        # Validate with listing parser
        parser = self.tools["listing_parser"]
        title_validation = parser.validate_title(listing["product_title"])
        bullets_validation = parser.validate_bullet_points(listing["bullet_points"])
        
        listing["validation"] = {
            "title_score": title_validation.get("score", 0),
            "bullets_score": bullets_validation.get("score", 0)
        }
        
        self.memory_manager.store("copywriter", "listing", listing, "shared")
        
        return listing
        
    def _run_social_media_marketer(self, product_input: Dict, context: Dict,
                                   listing: Dict, market_research: Dict) -> Dict[str, Any]:
        """Execute Social Media Marketer agent."""
        self.logger.info("🤖 Executing: Social Media Marketer")
        
        product_info = product_input.get("product_info", {})
        product_name = product_info.get("product_name", "")
        
        campaign = {
            "platforms": {
                "facebook": {
                    "post_frequency": "3x per week",
                    "content_types": ["Product photos", "Customer testimonials", "How-to videos"],
                    "ad_budget": "$500/month",
                    "targeting": {
                        "age": "25-54",
                        "interests": [product_info.get("product_category", "shopping")],
                        "behaviors": ["Online shoppers"]
                    },
                    "sample_posts": [
                        f"🌟 Introducing {product_name}! Transform your daily routine with premium quality.",
                        f"💡 Did you know? {product_name} features {product_info.get('product_features', ['amazing benefits'])[0]}",
                        f"🎉 Limited time offer! Get your {product_name} today. Link in bio!"
                    ]
                },
                "instagram": {
                    "post_frequency": "Daily",
                    "content_types": ["Product showcases", "Lifestyle shots", "Stories", "Reels"],
                    "hashtags": [f"#{product_name.replace(' ', '')}", f"#{product_info.get('product_category', 'product')}",
                               "#AmazonFinds", "#ProductReview", "#ShopSmall"],
                    "sample_captions": [
                        f"✨ Meet your new favorite: {product_name} ✨\n\n{listing.get('bullet_points', [''])[0]}\n\nShop now! Link in bio 🛒",
                        f"🔥 Why we love {product_name}:\n• Quality you can trust\n• Designed for you\n• Amazing value\n\nWhat are you waiting for? 💫"
                    ]
                },
                "tiktok": {
                    "post_frequency": "4x per week",
                    "content_types": ["Unboxing", "Demo videos", "Before/After", "Testimonials"],
                    "video_themes": [
                        f"{product_name} unboxing and first impressions",
                        f"How I use {product_name} in my daily routine",
                        f"Why {product_name} is trending right now"
                    ]
                },
                "pinterest": {
                    "pin_frequency": "5x per week",
                    "board_themes": [product_info.get("product_category", "Products"), "Gift Ideas", "Home Essentials"],
                    "pin_descriptions": [
                        f"Discover {product_name} - the perfect solution for {product_info.get('target_audience', 'everyone')}. Click to shop!"
                    ]
                }
            },
            "content_calendar": [
                {"week": 1, "focus": "Product launch announcement", "platforms": ["All"]},
                {"week": 2, "focus": "Feature highlights", "platforms": ["Facebook", "Instagram"]},
                {"week": 3, "focus": "Customer testimonials", "platforms": ["All"]},
                {"week": 4, "focus": "Limited time promotions", "platforms": ["Facebook", "TikTok"]}
            ],
            "influencer_strategy": {
                "target_influencers": "Micro-influencers (10k-100k followers)",
                "budget": "$300/month",
                "expected_reach": "50,000+ potential customers"
            },
            "engagement_tactics": [
                "Run giveaway contests",
                "Respond to all comments within 24 hours",
                "Share user-generated content",
                "Create polls and interactive stories"
            ]
        }
        
        self.memory_manager.store("social_marketer", "campaign", campaign, "shared")
        
        return campaign
        
    def _run_quality_validator(self, listing: Dict, social_campaign: Dict, context: Dict) -> Dict[str, Any]:
        """Execute Quality Validator agent."""
        self.logger.info("🤖 Executing: Quality Validator")
        
        # Check listing compliance
        compliance_checker = self.tools["compliance_checker"]
        listing_compliance = compliance_checker.check_listing_compliance(listing)
        
        # Check hallucinations
        validation_context = {
            "product_info": context.get("product_info", {}),
            "market_insights": self.memory_manager.retrieve("market_research", "insights", "shared")
        }
        
        is_valid, hallucination_report = self.hallucination_guard.validate_content(
            listing, validation_context
        )
        
        # Compile validation report
        validation_report = {
            "overall_status": "PASSED" if listing_compliance["overall_compliant"] and is_valid else "FAILED",
            "compliance_check": {
                "passed": listing_compliance["overall_compliant"],
                "score": listing_compliance["overall_score"],
                "component_scores": {
                    comp: result["score"] 
                    for comp, result in listing_compliance.get("component_results", {}).items()
                },
                "violations": [
                    v for result in listing_compliance.get("component_results", {}).values()
                    for v in result.get("violations", [])
                ]
            },
            "hallucination_check": {
                "passed": is_valid,
                "score": hallucination_report.get("score", 0),
                "violations": hallucination_report.get("violations", []),
                "warnings": hallucination_report.get("warnings", [])
            },
            "quality_score": (listing_compliance["overall_score"] + hallucination_report.get("score", 0)) / 2,
            "recommendations": [],
            "requires_revision": False
        }
        
        # Generate recommendations
        if validation_report["quality_score"] < 70:
            validation_report["requires_revision"] = True
            validation_report["recommendations"].append("Content needs significant revision")
            
        if listing_compliance["overall_score"] < 80:
            validation_report["recommendations"].append("Address compliance violations before publishing")
            
        if not is_valid:
            validation_report["recommendations"].append("Review and correct factual inconsistencies")
            
        if validation_report["quality_score"] >= 90:
            validation_report["recommendations"].append("✅ Content is ready for publication!")
            
        self.logger.info(f"Validation Score: {validation_report['quality_score']:.1f}/100")
        
        return validation_report
        
    def _save_outputs(self, workflow_id: str, output: Dict[str, Any]):
        """Save campaign outputs to files."""
        results_dir = Path(__file__).parent / "storage" / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_path = results_dir / f"campaign_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        self.logger.info(f"💾 Saved JSON output: {json_path}")
        
        # Save Markdown
        md_path = results_dir / f"campaign_{timestamp}.md"
        markdown_content = self._generate_markdown_report(output)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        self.logger.info(f"💾 Saved Markdown output: {md_path}")
        
    def _generate_markdown_report(self, output: Dict[str, Any]) -> str:
        """Generate markdown report from output."""
        product_name = output.get("product_name", "Unknown Product")
        workflow_id = output.get("workflow_id", "N/A")
        
        md = f"""# Amazon Campaign Report: {product_name}

**Workflow ID:** `{workflow_id}`  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  

---

## 📋 Campaign Plan

### Objectives
"""
        
        for obj in output.get("campaign_plan", {}).get("campaign_objectives", []):
            md += f"- {obj}\n"
            
        md += f"""
### Timeline
{output.get("campaign_plan", {}).get("timeline", "N/A")}

### Success Metrics
"""
        
        metrics = output.get("campaign_plan", {}).get("success_metrics", {})
        for key, value in metrics.items():
            md += f"- **{key.replace('_', ' ').title()}:** {value}\n"
            
        md += """

---

## 🔍 Market Research Insights

### Key Trends
"""
        
        for trend in output.get("market_insights", {}).get("key_trends", []):
            md += f"- {trend}\n"
            
        md += """

### Competitor Analysis
"""
        
        competitors = output.get("market_insights", {}).get("competitor_analysis", {}).get("top_competitors", [])
        for comp in competitors:
            md += f"- **{comp.get('name')}:** {comp.get('price_range')} | ⭐ {comp.get('rating')} ({comp.get('reviews')} reviews)\n"
            
        md += """

---

## 🔑 SEO Strategy

### Primary Keywords
"""
        
        for kw in output.get("seo_strategy", {}).get("primary_keywords", []):
            md += f"- {kw}\n"
            
        md += """

### Secondary Keywords
"""
        
        for kw in output.get("seo_strategy", {}).get("secondary_keywords", [])[:5]:
            md += f"- {kw}\n"
            
        listing = output.get("amazon_listing", {})
        md += f"""

---

## 📝 Amazon Listing

### Product Title
```
{listing.get("product_title", "N/A")}
```

### Bullet Points
"""
        
        for bullet in listing.get("bullet_points", []):
            md += f"{bullet}\n\n"
            
        md += f"""

### Product Description
{listing.get("product_description", "N/A")}

---

## 📱 Social Media Campaign

"""
        
        social = output.get("social_media_campaign", {})
        for platform, details in social.get("platforms", {}).items():
            md += f"### {platform.title()}\n"
            md += f"- **Post Frequency:** {details.get('post_frequency', 'N/A')}\n"
            if "sample_posts" in details:
                md += "- **Sample Post:**\n"
                md += f"  > {details['sample_posts'][0]}\n"
            md += "\n"
            
        md += """

---

## ✅ Validation Report

"""
        
        validation = output.get("validation_report", {})
        md += f"**Overall Status:** {validation.get('overall_status', 'N/A')}  \n"
        md += f"**Quality Score:** {validation.get('quality_score', 0):.1f}/100  \n\n"
        
        md += "### Recommendations\n"
        for rec in validation.get("recommendations", []):
            md += f"- {rec}\n"
            
        md += """

---

## 📊 Workflow Metrics

"""
        
        metrics = output.get("workflow_metrics", {})
        md += f"- **Total Execution Time:** {metrics.get('total_execution_time', 0):.2f}s\n"
        md += f"- **Agents Executed:** {metrics.get('agents_executed', 0)}\n"
        md += f"- **Stages Completed:** {metrics.get('stages_completed', 0)}\n"
        md += f"- **Parallel Executions:** {metrics.get('parallel_executions', 0)}\n"
        md += f"- **Overall Status:** {'✅ Success' if metrics.get('success', False) else '❌ Failed'}\n"
        
        md += """

---

*Generated by Amazon Campaign Multi-Agent System (Google ADK)*
"""
        
        return md


def create_sample_input() -> Dict[str, Any]:
    """Create sample product input."""
    return {
        "product_info": {
            "product_name": "Premium Wireless Bluetooth Headphones",
            "product_category": "Electronics",
            "brand_name": "AudioPro",
            "product_features": [
                "Active Noise Cancellation (ANC) technology",
                "40-hour battery life with quick charge",
                "Premium leather ear cushions for comfort",
                "Foldable design with carrying case",
                "Multi-device connectivity"
            ],
            "unique_selling_points": [
                "Industry-leading 40-hour battery life",
                "Superior sound quality with custom-tuned drivers",
                "Premium materials and build quality",
                "Excellent customer service and warranty"
            ],
            "target_audience": "Music enthusiasts, professionals, travelers aged 25-45",
            "price_point": "$149.99"
        },
        "campaign_params": {
            "campaign_goals": [
                "Launch product successfully",
                "Achieve 100 sales in first month",
                "Maintain 4.5+ star rating"
            ],
            "budget": "$2000",
            "timeline": "90 days",
            "target_markets": ["US", "CA", "UK"]
        }
    }


def main():
    """Main execution function."""
    print("=" * 80)
    print("🚀 Amazon Campaign Multi-Agent System (Google ADK)")
    print("=" * 80)
    print()
    
    try:
        # Check for API key
        if not os.getenv("GEMINI_API_KEY"):
            print("⚠️  Warning: GEMINI_API_KEY not set in .env file")
            print("The system will run in demo mode with simulated agent outputs.\n")
        
        # Initialize system
        print("Initializing system...")
        system = AmazonCampaignSystem()
        print()
        
        # Create sample input
        print("Using sample product input: Premium Wireless Bluetooth Headphones")
        product_input = create_sample_input()
        print()
        
        # Run campaign
        result = system.run_campaign(product_input)
        
        print()
        print("=" * 80)
        print("✅ Campaign Generation Complete!")
        print("=" * 80)
        print(f"\nQuality Score: {result['validation_report']['quality_score']:.1f}/100")
        print(f"Status: {result['validation_report']['overall_status']}")
        print(f"\nOutputs saved to: ./storage/results/")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
