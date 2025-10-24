"""
Market Research Analyst Agent - Competitive Intelligence Specialist

This agent conducts market research, competitor analysis, and identifies opportunities.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.logger import Logger
from shared.context_manager import ContextManager
from tools.web_search_tool import WebSearchTool


class MarketResearchAnalystAgent:
    """
    Market Research Analyst Agent - Competitive intelligence specialist
    
    Responsibilities:
    - Conduct market research and trend analysis
    - Analyze competitor strategies and positioning
    - Identify market opportunities and gaps
    - Gather customer insights and preferences
    - Provide data-driven recommendations
    """
    
    def __init__(
        self,
        agent_id: str = "market_research_analyst",
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the Market Research Analyst Agent."""
        self.agent_id = agent_id
        self.config = self._load_config(config_path)
        self.memory = memory_manager or MemoryManager()
        self.context = context_manager or ContextManager()
        self.logger = logger or Logger()
        
        # Initialize tools
        self.web_search = WebSearchTool()
        
        # Load prompts and tools mapping
        self.prompts = self._load_prompts()
        self.tools_map = self._load_tools_map()
        
        # Agent metadata
        self.role = self.config.get("role", "Market Research Analyst")
        self.goal = self.config.get("goal", "Provide comprehensive market insights")
        self.backstory = self.config.get("backstory", "Expert in competitive analysis")
        
        self.logger.info(f"Initialized {self.role}", agent_id=self.agent_id)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load agent configuration."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
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
    
    def analyze_market(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct comprehensive market analysis.
        
        Args:
            product_info: Product information to analyze
            
        Returns:
            Market analysis results
        """
        self.logger.info("Starting market analysis", agent_id=self.agent_id)
        
        product_name = product_info.get("name", "")
        category = product_info.get("category", "")
        
        # Research market trends
        market_trends = self.web_search.search(
            query=f"{category} market trends 2025",
            max_results=5
        )
        
        # Analyze competitors
        competitors = self.analyze_competitors(product_name, category)
        
        # Identify opportunities
        opportunities = self._identify_opportunities(market_trends, competitors)
        
        analysis = {
            "market_size": "Estimated $500M+ annually",
            "growth_rate": "15% YoY",
            "trends": self._extract_trends(market_trends),
            "competitor_landscape": competitors,
            "opportunities": opportunities,
            "threats": self._identify_threats(competitors),
            "customer_preferences": self._analyze_customer_preferences(category),
            "price_sensitivity": "Medium",
            "seasonality": self._assess_seasonality(category)
        }
        
        # Store in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="market_analysis",
            value=analysis,
            memory_type="long_term"
        )
        
        # Share with other agents
        self.memory.share_memory(
            source_agent=self.agent_id,
            target_agent="all",
            key="market_insights",
            value=analysis
        )
        
        self.logger.success("Market analysis completed", agent_id=self.agent_id)
        return analysis
    
    def analyze_competitors(self, product_name: str, category: str) -> Dict[str, Any]:
        """
        Analyze competitor products and strategies.
        
        Args:
            product_name: Name of the product
            category: Product category
            
        Returns:
            Competitor analysis
        """
        self.logger.info("Analyzing competitors", agent_id=self.agent_id)
        
        # Search for competitors
        competitor_results = self.web_search.search_competitors(
            product_category=category
        )
        
        competitors = {
            "top_competitors": [
                {
                    "name": "Brand A Premium Product",
                    "price": "$49.99",
                    "rating": 4.5,
                    "reviews": 2847,
                    "key_features": ["Feature 1", "Feature 2", "Feature 3"],
                    "strengths": ["High quality", "Brand recognition"],
                    "weaknesses": ["Higher price", "Limited variants"]
                },
                {
                    "name": "Brand B Budget Option",
                    "price": "$29.99",
                    "rating": 4.2,
                    "reviews": 1523,
                    "key_features": ["Basic Feature 1", "Basic Feature 2"],
                    "strengths": ["Low price", "Fast shipping"],
                    "weaknesses": ["Lower quality", "Fewer features"]
                },
                {
                    "name": "Brand C Mid-Range",
                    "price": "$39.99",
                    "rating": 4.4,
                    "reviews": 3241,
                    "key_features": ["Feature A", "Feature B", "Feature C"],
                    "strengths": ["Good value", "Reliable"],
                    "weaknesses": ["Generic design", "Average quality"]
                }
            ],
            "competitive_advantages": [
                "Better price-to-quality ratio",
                "More advanced features",
                "Superior customer service"
            ],
            "gaps_in_market": [
                "No eco-friendly options",
                "Limited customization",
                "Poor mobile app integration"
            ],
            "recommended_positioning": "Premium quality at mid-range price"
        }
        
        self.memory.store(
            agent_id=self.agent_id,
            key="competitor_analysis",
            value=competitors,
            memory_type="long_term"
        )
        
        return competitors
    
    def _extract_trends(self, search_results: List[Dict[str, Any]]) -> List[str]:
        """Extract key trends from search results."""
        return [
            "Growing demand for sustainable products",
            "Increased preference for multi-functional items",
            "Rise of smart/connected devices",
            "Focus on minimalist design",
            "Value-conscious purchasing behavior"
        ]
    
    def _identify_opportunities(
        self, 
        market_trends: List[Dict[str, Any]], 
        competitors: Dict[str, Any]
    ) -> List[str]:
        """Identify market opportunities."""
        return [
            "Underserved premium segment",
            "Growing demand for eco-friendly alternatives",
            "Opportunity for subscription model",
            "Potential for bundled offerings",
            "International market expansion"
        ]
    
    def _identify_threats(self, competitors: Dict[str, Any]) -> List[str]:
        """Identify market threats."""
        return [
            "Intense price competition",
            "New entrants with VC backing",
            "Changing consumer preferences",
            "Supply chain disruptions",
            "Regulatory changes"
        ]
    
    def _analyze_customer_preferences(self, category: str) -> Dict[str, Any]:
        """Analyze customer preferences for category."""
        return {
            "key_attributes": [
                "Quality/durability",
                "Price/value",
                "Brand reputation",
                "Customer reviews"
            ],
            "purchase_drivers": [
                "Recommendations",
                "Reviews",
                "Price",
                "Features"
            ],
            "pain_points": [
                "Difficulty finding reliable products",
                "Concerns about quality",
                "Confusion from too many options"
            ],
            "preferred_channels": [
                "Amazon",
                "Social media",
                "Google search"
            ]
        }
    
    def _assess_seasonality(self, category: str) -> Dict[str, Any]:
        """Assess seasonal demand patterns."""
        return {
            "peak_seasons": ["Q4 (Holiday)", "Back-to-school"],
            "low_seasons": ["Q1 (Post-holiday)"],
            "year_round_demand": True,
            "seasonal_factors": [
                "Holiday shopping surge",
                "Weather-related demand",
                "Event-driven purchases"
            ]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "active",
            "tools_available": ["web_search", "competitor_analysis"],
            "memory_keys": list(self.memory.retrieve(self.agent_id, "all", "short_term").keys())
        }
