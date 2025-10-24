"""
Copywriter Agent - Amazon Listing Content Creator

This agent creates compelling Amazon listing content including titles, bullet points, and descriptions.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.logger import Logger
from shared.context_manager import ContextManager
from tools.amazon_listing_parser import AmazonListingParser


class CopywriterAgent:
    """
    Copywriter Agent - Amazon listing content creator
    
    Responsibilities:
    - Write compelling product titles
    - Create persuasive bullet points
    - Craft detailed product descriptions
    - Maintain brand voice and tone
    - Optimize for conversions
    """
    
    def __init__(
        self,
        agent_id: str = "copywriter",
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the Copywriter Agent."""
        self.agent_id = agent_id
        self.config = self._load_config(config_path)
        self.memory = memory_manager or MemoryManager()
        self.context = context_manager or ContextManager()
        self.logger = logger or Logger()
        
        # Initialize tools
        self.listing_parser = AmazonListingParser()
        
        # Load prompts and tools mapping
        self.prompts = self._load_prompts()
        self.tools_map = self._load_tools_map()
        
        # Agent metadata
        self.role = self.config.get("role", "Copywriter")
        self.goal = self.config.get("goal", "Create compelling listing content")
        self.backstory = self.config.get("backstory", "Expert copywriter")
        
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
    
    def create_amazon_listing(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create complete Amazon listing content.
        
        Args:
            product_info: Product information and research data
            
        Returns:
            Complete listing content
        """
        self.logger.info("Creating Amazon listing content", agent_id=self.agent_id)
        
        # Retrieve SEO keywords and market insights
        keywords = self.memory.retrieve(
            agent_id="seo_specialist",
            key="keyword_research",
            memory_type="long_term"
        ) or {}
        
        market_insights = self.memory.retrieve(
            agent_id="market_research_analyst",
            key="market_analysis",
            memory_type="long_term"
        ) or {}
        
        # Create listing components
        title = self.write_title(product_info, keywords)
        bullet_points = self.write_bullet_points(product_info, keywords, market_insights)
        description = self.write_description(product_info, keywords, market_insights)
        
        # Validate listing
        title_validation = self.listing_parser.validate_title(title)
        bullets_validation = self.listing_parser.validate_bullet_points(bullet_points)
        description_validation = self.listing_parser.validate_description(description)
        
        listing = {
            "title": title,
            "title_validation": title_validation,
            "bullet_points": bullet_points,
            "bullets_validation": bullets_validation,
            "description": description,
            "description_validation": description_validation,
            "a_plus_content": self._create_a_plus_content(product_info),
            "search_terms": self._generate_search_terms(keywords),
            "overall_score": self._calculate_listing_score(
                title_validation, bullets_validation, description_validation
            )
        }
        
        # Store in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="amazon_listing",
            value=listing,
            memory_type="long_term"
        )
        
        # Share with other agents
        self.memory.share_memory(
            source_agent=self.agent_id,
            target_agent="all",
            key="listing_content",
            value=listing
        )
        
        self.logger.success("Amazon listing created", agent_id=self.agent_id)
        return listing
    
    def write_title(self, product_info: Dict[str, Any], keywords: Dict[str, Any]) -> str:
        """
        Write optimized product title.
        
        Args:
            product_info: Product information
            keywords: SEO keywords
            
        Returns:
            Optimized title
        """
        product_name = product_info.get("name", "Premium Product")
        category = product_info.get("category", "General")
        features = product_info.get("features", [])
        
        # Get primary keywords
        primary_keywords = keywords.get("primary_keywords", [])
        top_keyword = primary_keywords[0]["keyword"] if primary_keywords else ""
        
        # Construct title with keywords and key features
        key_features = features[:2] if isinstance(features, list) else []
        features_text = ", ".join(key_features) if key_features else "High Quality, Durable"
        
        title = f"{top_keyword if top_keyword else product_name} - {features_text} - Perfect for {category} - 2025 Edition"
        
        # Ensure title is within character limit (200)
        if len(title) > 200:
            title = title[:197] + "..."
        
        return title
    
    def write_bullet_points(
        self, 
        product_info: Dict[str, Any], 
        keywords: Dict[str, Any],
        market_insights: Dict[str, Any]
    ) -> List[str]:
        """
        Write persuasive bullet points.
        
        Args:
            product_info: Product information
            keywords: SEO keywords
            market_insights: Market research data
            
        Returns:
            List of bullet points
        """
        features = product_info.get("features", [])
        benefits = product_info.get("benefits", [])
        
        # Get secondary keywords
        secondary_keywords = keywords.get("secondary_keywords", [])
        
        bullets = []
        
        # Bullet 1: Primary benefit with keyword
        bullets.append(
            f"✓ PREMIUM QUALITY CONSTRUCTION: Made with high-grade materials ensuring durability and long-lasting performance. "
            f"{secondary_keywords[0]['keyword'] if secondary_keywords else 'Professional grade'} design for demanding applications."
        )
        
        # Bullet 2: Key feature with benefit
        bullets.append(
            f"✓ ADVANCED FEATURES: Equipped with state-of-the-art technology including "
            f"{features[0] if features else 'innovative design'}, {features[1] if len(features) > 1 else 'superior functionality'}, "
            f"and user-friendly interface for maximum convenience."
        )
        
        # Bullet 3: Value proposition
        bullets.append(
            f"✓ EXCEPTIONAL VALUE: Get premium performance at a competitive price. "
            f"Includes comprehensive warranty, responsive customer support, and satisfaction guarantee. "
            f"Save time and money with this cost-effective solution."
        )
        
        # Bullet 4: Problem solution
        bullets.append(
            f"✓ SOLVES YOUR NEEDS: Specifically designed to address common challenges in {product_info.get('category', 'your field')}. "
            f"Eliminates frustration, improves efficiency, and delivers consistent results every time."
        )
        
        # Bullet 5: Social proof and guarantee
        bullets.append(
            f"✓ TRUSTED BY THOUSANDS: Join satisfied customers who rate us 5-stars. "
            f"Backed by 30-day money-back guarantee and lifetime customer support. "
            f"Order now with confidence and experience the difference!"
        )
        
        return bullets
    
    def write_description(
        self, 
        product_info: Dict[str, Any], 
        keywords: Dict[str, Any],
        market_insights: Dict[str, Any]
    ) -> str:
        """
        Write detailed product description.
        
        Args:
            product_info: Product information
            keywords: SEO keywords
            market_insights: Market research data
            
        Returns:
            Complete description
        """
        product_name = product_info.get("name", "Our Premium Product")
        category = product_info.get("category", "General")
        features = product_info.get("features", [])
        
        description = f"""
<h1>Transform Your {category} Experience with {product_name}</h1>

<p>Discover the ultimate solution for your {category} needs. Our {product_name} combines cutting-edge technology 
with premium craftsmanship to deliver unmatched performance and reliability.</p>

<h2>Why Choose Our Product?</h2>

<p><b>Premium Quality Materials:</b> Crafted from the finest materials, ensuring durability and longevity. 
Each unit undergoes rigorous quality control to meet our exacting standards.</p>

<p><b>Advanced Features:</b> Equipped with innovative features including {features[0] if features else 'state-of-the-art technology'}, 
{features[1] if len(features) > 1 else 'user-friendly design'}, and {features[2] if len(features) > 2 else 'superior performance'}.</p>

<p><b>Exceptional Value:</b> Get professional-grade performance without the premium price tag. 
We believe quality should be accessible to everyone.</p>

<h2>Perfect For:</h2>
<ul>
<li>Home and professional use</li>
<li>Daily tasks and special projects</li>
<li>Beginners and experienced users</li>
<li>Indoor and outdoor applications</li>
</ul>

<h2>What's Included:</h2>
<ul>
<li>1x {product_name}</li>
<li>Comprehensive user manual</li>
<li>Quick start guide</li>
<li>Warranty card</li>
<li>Dedicated customer support</li>
</ul>

<h2>Our Guarantee:</h2>

<p>We stand behind our products with a 30-day money-back guarantee and lifetime customer support. 
If you're not completely satisfied, we'll make it right.</p>

<p><b>Order now and experience the difference!</b> Join thousands of satisfied customers who have made the smart choice.</p>

<h2>Specifications:</h2>
<p>Category: {category}<br>
Material: Premium grade<br>
Durability: Heavy-duty construction<br>
Warranty: Comprehensive coverage<br>
Support: Lifetime assistance</p>
"""
        
        return description.strip()
    
    def _create_a_plus_content(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create A+ Content structure."""
        return {
            "module_1": {
                "type": "comparison_table",
                "title": "Why We're Better",
                "content": "Side-by-side comparison with competitors"
            },
            "module_2": {
                "type": "feature_spotlight",
                "title": "Key Features",
                "content": "Detailed feature descriptions with images"
            },
            "module_3": {
                "type": "lifestyle_images",
                "title": "See It In Action",
                "content": "Product in real-world scenarios"
            },
            "module_4": {
                "type": "brand_story",
                "title": "Our Story",
                "content": "Brand values and mission"
            }
        }
    
    def _generate_search_terms(self, keywords: Dict[str, Any]) -> List[str]:
        """Generate backend search terms."""
        backend = keywords.get("backend_keywords", [])
        long_tail = keywords.get("long_tail_keywords", [])
        
        search_terms = []
        
        # Add backend keywords
        if isinstance(backend, list):
            search_terms.extend(backend[:50])
        
        # Add long-tail keywords
        if isinstance(long_tail, list):
            for item in long_tail[:20]:
                if isinstance(item, dict) and "keyword" in item:
                    search_terms.append(item["keyword"])
        
        # Remove duplicates and limit to 250 bytes
        search_terms = list(set(search_terms))
        combined = " ".join(search_terms)
        
        if len(combined.encode('utf-8')) > 249:
            # Truncate to fit byte limit
            search_terms = search_terms[:30]
        
        return search_terms
    
    def _calculate_listing_score(
        self,
        title_validation: Dict[str, Any],
        bullets_validation: Dict[str, Any],
        description_validation: Dict[str, Any]
    ) -> int:
        """Calculate overall listing quality score."""
        title_score = title_validation.get("score", 0)
        bullets_score = bullets_validation.get("score", 0)
        description_score = description_validation.get("score", 0)
        
        # Weighted average
        overall = (title_score * 0.3 + bullets_score * 0.4 + description_score * 0.3)
        
        return int(overall)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "active",
            "tools_available": ["listing_parser", "content_generator"],
            "memory_keys": list(self.memory.retrieve(self.agent_id, "all", "short_term").keys())
        }
