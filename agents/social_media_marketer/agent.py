"""
Social Media Marketer Agent - Multi-Platform Campaign Designer

This agent creates comprehensive social media marketing campaigns across multiple platforms.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.logger import Logger
from shared.context_manager import ContextManager


class SocialMediaMarketerAgent:
    """
    Social Media Marketer Agent - Multi-platform campaign designer
    
    Responsibilities:
    - Design Facebook advertising campaigns
    - Create Instagram content strategies
    - Develop TikTok video concepts
    - Plan Pinterest marketing boards
    - Coordinate cross-platform campaigns
    """
    
    def __init__(
        self,
        agent_id: str = "social_media_marketer",
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the Social Media Marketer Agent."""
        self.agent_id = agent_id
        self.config = self._load_config(config_path)
        self.memory = memory_manager or MemoryManager()
        self.context = context_manager or ContextManager()
        self.logger = logger or Logger()
        
        # Load prompts and tools mapping
        self.prompts = self._load_prompts()
        self.tools_map = self._load_tools_map()
        
        # Agent metadata
        self.role = self.config.get("role", "Social Media Marketer")
        self.goal = self.config.get("goal", "Create engaging social campaigns")
        self.backstory = self.config.get("backstory", "Expert social media strategist")
        
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
    
    def create_social_campaigns(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive multi-platform social media campaigns.
        
        Args:
            product_info: Product information
            
        Returns:
            Complete social media campaign strategy
        """
        self.logger.info("Creating social media campaigns", agent_id=self.agent_id)
        
        # Retrieve listing content
        listing = self.memory.retrieve(
            agent_id="copywriter",
            key="amazon_listing",
            memory_type="long_term"
        ) or {}
        
        # Retrieve market insights
        market_insights = self.memory.retrieve(
            agent_id="market_research_analyst",
            key="market_analysis",
            memory_type="long_term"
        ) or {}
        
        campaigns = {
            "facebook_campaign": self.create_facebook_campaign(product_info, listing),
            "instagram_campaign": self.create_instagram_campaign(product_info, listing),
            "tiktok_campaign": self.create_tiktok_campaign(product_info, listing),
            "pinterest_campaign": self.create_pinterest_campaign(product_info, listing),
            "content_calendar": self._create_content_calendar(),
            "budget_allocation": self._calculate_budget_allocation(),
            "kpis": self._define_kpis(),
            "posting_schedule": self._create_posting_schedule()
        }
        
        # Store in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="social_campaigns",
            value=campaigns,
            memory_type="long_term"
        )
        
        # Share with other agents
        self.memory.share_memory(
            source_agent=self.agent_id,
            target_agent="all",
            key="social_media_strategy",
            value=campaigns
        )
        
        self.logger.success("Social media campaigns created", agent_id=self.agent_id)
        return campaigns
    
    def create_facebook_campaign(
        self, 
        product_info: Dict[str, Any], 
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Facebook advertising campaign."""
        product_name = product_info.get("name", "Our Product")
        
        return {
            "campaign_objective": "Conversions",
            "target_audience": {
                "age_range": "25-54",
                "interests": ["shopping", "amazon", product_info.get("category", "general")],
                "behaviors": ["online shoppers", "engaged shoppers"],
                "demographics": "All genders, middle to upper income"
            },
            "ad_sets": [
                {
                    "name": "Awareness - Cold Traffic",
                    "budget": "$50/day",
                    "placement": ["Feed", "Stories", "Marketplace"],
                    "optimization": "Reach"
                },
                {
                    "name": "Consideration - Warm Traffic",
                    "budget": "$75/day",
                    "placement": ["Feed", "Stories"],
                    "optimization": "Link Clicks"
                },
                {
                    "name": "Conversion - Hot Traffic",
                    "budget": "$100/day",
                    "placement": ["Feed"],
                    "optimization": "Conversions"
                }
            ],
            "ad_creatives": [
                {
                    "format": "Carousel",
                    "headline": f"Discover {product_name} - Top Rated on Amazon",
                    "primary_text": "Transform your life with our premium product. Limited time offer!",
                    "cta": "Shop Now",
                    "images": "Product + lifestyle shots"
                },
                {
                    "format": "Video",
                    "headline": f"See {product_name} in Action",
                    "primary_text": "Watch how easy it is to use. Join thousands of satisfied customers!",
                    "cta": "Learn More",
                    "video": "Product demo + testimonials"
                },
                {
                    "format": "Single Image",
                    "headline": "⭐ 5-Star Amazon Bestseller",
                    "primary_text": "Don't miss out! Grab yours before stock runs out.",
                    "cta": "Buy Now",
                    "image": "Hero product shot"
                }
            ],
            "retargeting": {
                "website_visitors": "Show to visitors from last 30 days",
                "video_viewers": "Target 50%+ video viewers",
                "engaged_users": "Target post engagers"
            },
            "estimated_reach": "50,000-75,000 people per week",
            "expected_ctr": "2.5-3.5%",
            "expected_roas": "3.5x-5x"
        }
    
    def create_instagram_campaign(
        self, 
        product_info: Dict[str, Any], 
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Instagram content strategy."""
        return {
            "content_pillars": [
                "Product Features",
                "Customer Stories",
                "Behind the Scenes",
                "Educational Content",
                "Lifestyle Integration"
            ],
            "feed_posts": [
                {
                    "type": "Product Showcase",
                    "caption": "✨ Introducing our game-changer! Swipe to see all the amazing features. Link in bio! #amazon #newproduct",
                    "hashtags": ["#amazonfinds", "#musthave", "#shopping", "#productreview"],
                    "frequency": "3x per week"
                },
                {
                    "type": "User Generated Content",
                    "caption": "💙 Our customers love us! Thanks @customer for sharing. Tag us for a chance to be featured!",
                    "hashtags": ["#customerreview", "#happycustomer", "#testimonial"],
                    "frequency": "2x per week"
                },
                {
                    "type": "Educational Tips",
                    "caption": "📚 Pro tip: Here's how to get the most out of your product. Save this for later!",
                    "hashtags": ["#protip", "#howtouse", "#tutorial"],
                    "frequency": "2x per week"
                }
            ],
            "stories": {
                "daily_content": [
                    "Product highlights",
                    "Customer testimonials",
                    "Behind-the-scenes",
                    "Polls and Q&A",
                    "Limited offers"
                ],
                "highlights": [
                    "Products",
                    "Reviews",
                    "How-To",
                    "FAQs",
                    "Offers"
                ]
            },
            "reels": [
                {
                    "concept": "Unboxing Experience",
                    "duration": "15-30 seconds",
                    "music": "Trending audio",
                    "hook": "Wait for the end! 😱"
                },
                {
                    "concept": "Before/After Transformation",
                    "duration": "15-20 seconds",
                    "music": "Upbeat trending",
                    "hook": "You won't believe the difference!"
                },
                {
                    "concept": "Quick Tutorial",
                    "duration": "30-45 seconds",
                    "music": "Informative background",
                    "hook": "Learn this in 30 seconds!"
                }
            ],
            "influencer_strategy": {
                "micro_influencers": "10-50k followers, 3-5 partnerships",
                "content_creators": "Authentic reviews and tutorials",
                "budget": "$500-1000 per partnership",
                "deliverables": "1 feed post + 3 stories"
            },
            "engagement_tactics": [
                "Reply to all comments within 2 hours",
                "Host weekly giveaways",
                "Create interactive polls/quizzes",
                "Share user-generated content",
                "Use Instagram Shopping tags"
            ]
        }
    
    def create_tiktok_campaign(
        self, 
        product_info: Dict[str, Any], 
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create TikTok video strategy."""
        return {
            "video_concepts": [
                {
                    "title": "Amazon Find Alert! 🚨",
                    "hook": "You NEED this from Amazon!",
                    "content": "Quick product demo showing key features",
                    "cta": "Link in bio to shop!",
                    "trending_sound": "Use current viral audio",
                    "hashtags": ["#amazonfind", "#amazonmusthaves", "#tiktokmademebuyit"]
                },
                {
                    "title": "Problem → Solution",
                    "hook": "Struggling with [problem]?",
                    "content": "Show problem then product solving it",
                    "cta": "Get yours now!",
                    "trending_sound": "Transformation audio",
                    "hashtags": ["#problemsolved", "#lifehack", "#amazonfinds"]
                },
                {
                    "title": "5-Star Review Reaction",
                    "hook": "Reading your 5-star reviews! 🌟",
                    "content": "React to real customer reviews",
                    "cta": "Thank you for the love!",
                    "trending_sound": "Emotional music",
                    "hashtags": ["#customerreview", "#5stars", "#grateful"]
                }
            ],
            "posting_strategy": {
                "frequency": "2-3 videos per day",
                "best_times": ["7-9 AM", "12-2 PM", "7-10 PM"],
                "video_length": "15-45 seconds",
                "first_3_seconds": "Critical hook to stop scrolling"
            },
            "tiktok_shop_integration": {
                "product_showcase": "Enable TikTok Shop if available",
                "live_shopping": "Weekly live sessions showing product",
                "affiliate_program": "Partner with TikTok creators"
            },
            "challenges": {
                "branded_hashtag": "#[ProductName]Challenge",
                "participation_incentive": "Feature best videos",
                "ugc_generation": "Encourage customers to create content"
            },
            "estimated_views": "100k-500k per video with viral potential",
            "engagement_rate": "5-8% (higher than other platforms)"
        }
    
    def create_pinterest_campaign(
        self, 
        product_info: Dict[str, Any], 
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Pinterest marketing strategy."""
        return {
            "boards": [
                {
                    "name": f"{product_info.get('name', 'Product')} Collection",
                    "description": "Discover our full range of premium products",
                    "pins": "Product images, infographics, how-tos"
                },
                {
                    "name": "Customer Favorites",
                    "description": "See what our customers love most",
                    "pins": "Reviews, testimonials, user photos"
                },
                {
                    "name": "Tips & Tutorials",
                    "description": "Get the most out of your product",
                    "pins": "How-to guides, tips, best practices"
                }
            ],
            "pin_designs": [
                {
                    "type": "Product Pin",
                    "format": "Vertical (1000x1500px)",
                    "elements": "Product image + text overlay + branding",
                    "title": "Premium [Product] - Amazon Bestseller",
                    "description": "SEO-optimized description with keywords"
                },
                {
                    "type": "Infographic Pin",
                    "format": "Vertical (1000x2000px)",
                    "elements": "Data visualization + key benefits",
                    "title": "5 Reasons You Need This Product",
                    "description": "Detailed benefit breakdown"
                },
                {
                    "type": "Video Pin",
                    "format": "Square or vertical",
                    "elements": "Product demo + captions",
                    "title": "See It In Action",
                    "description": "Watch how easy it is to use"
                }
            ],
            "pinterest_ads": {
                "campaign_type": "Shopping Ads",
                "targeting": ["Keywords", "Interests", "Demographics"],
                "budget": "$25-50/day",
                "optimization": "Conversions"
            },
            "seo_strategy": {
                "keyword_optimization": "Use keywords in titles and descriptions",
                "rich_pins": "Enable product rich pins",
                "board_seo": "Optimize board names and descriptions"
            },
            "estimated_monthly_impressions": "50k-100k"
        }
    
    def _create_content_calendar(self) -> Dict[str, Any]:
        """Create 30-day content calendar."""
        return {
            "week_1": {
                "theme": "Launch & Awareness",
                "focus": "Introduce product, build excitement",
                "post_count": 14
            },
            "week_2": {
                "theme": "Education & Value",
                "focus": "Show benefits, tutorials, use cases",
                "post_count": 14
            },
            "week_3": {
                "theme": "Social Proof",
                "focus": "Reviews, testimonials, user content",
                "post_count": 14
            },
            "week_4": {
                "theme": "Conversion Push",
                "focus": "Limited offers, urgency, CTAs",
                "post_count": 14
            }
        }
    
    def _calculate_budget_allocation(self) -> Dict[str, Any]:
        """Calculate budget across platforms."""
        return {
            "facebook_ads": {"amount": "$1500/month", "percentage": "40%"},
            "instagram_ads": {"amount": "$1125/month", "percentage": "30%"},
            "tiktok_ads": {"amount": "$750/month", "percentage": "20%"},
            "pinterest_ads": {"amount": "$375/month", "percentage": "10%"},
            "influencer_marketing": {"amount": "$1000/month", "percentage": "Extra"},
            "content_creation": {"amount": "$500/month", "percentage": "Extra"},
            "total_monthly": "$5250"
        }
    
    def _define_kpis(self) -> Dict[str, Any]:
        """Define key performance indicators."""
        return {
            "primary_kpis": [
                {"metric": "Amazon Traffic", "target": "10,000 clicks/month"},
                {"metric": "Conversion Rate", "target": "3-5%"},
                {"metric": "ROAS", "target": "4x minimum"}
            ],
            "secondary_kpis": [
                {"metric": "Follower Growth", "target": "1000+/month"},
                {"metric": "Engagement Rate", "target": "5%+"},
                {"metric": "Video Views", "target": "100k+/month"},
                {"metric": "Link Clicks", "target": "5000+/month"}
            ],
            "monitoring": "Track daily via analytics dashboards"
        }
    
    def _create_posting_schedule(self) -> Dict[str, Any]:
        """Create optimal posting schedule."""
        return {
            "facebook": {
                "frequency": "1-2 posts/day",
                "best_times": ["1-3 PM", "7-9 PM"]
            },
            "instagram": {
                "feed": "1 post/day",
                "stories": "5-10/day",
                "reels": "3-4/week",
                "best_times": ["11 AM", "7-9 PM"]
            },
            "tiktok": {
                "frequency": "2-3 videos/day",
                "best_times": ["7-9 AM", "7-10 PM"]
            },
            "pinterest": {
                "frequency": "5-10 pins/day",
                "best_times": ["2-4 PM", "8-11 PM"]
            }
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "active",
            "platforms": ["Facebook", "Instagram", "TikTok", "Pinterest"],
            "memory_keys": list(self.memory.retrieve(self.agent_id, "all", "short_term").keys())
        }
