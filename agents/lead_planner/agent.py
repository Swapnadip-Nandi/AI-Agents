"""
Lead Planner Agent - Strategic Campaign Architect

This agent is responsible for analyzing the product, defining campaign objectives,
creating a strategic roadmap, and coordinating all other agents.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    # Fallback for development without ADK
    pass

from shared.memory_manager import MemoryManager
from shared.logger import Logger
from shared.context_manager import ContextManager


class LeadPlannerAgent:
    """
    Lead Planner Agent - Strategic campaign architect
    
    Responsibilities:
    - Analyze product information and market potential
    - Define campaign objectives and success criteria
    - Create strategic roadmap and timeline
    - Coordinate workflow between all agents
    - Make high-level strategic decisions
    """
    
    def __init__(
        self,
        agent_id: str = "lead_planner",
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        context_manager: Optional[ContextManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the Lead Planner Agent."""
        self.agent_id = agent_id
        self.config = self._load_config(config_path)
        self.memory = memory_manager or MemoryManager()
        self.context = context_manager or ContextManager()
        self.logger = logger or Logger()
        
        # Load prompts
        self.prompts = self._load_prompts()
        
        # Load tools mapping
        self.tools_map = self._load_tools_map()
        
        # Agent metadata
        self.role = self.config.get("role", "Strategic Campaign Architect")
        self.goal = self.config.get("goal", "Create comprehensive campaign strategy")
        self.backstory = self.config.get("backstory", "Expert campaign planner")
        
        self.logger.info(f"Initialized {self.role}", agent_id=self.agent_id)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load agent configuration from YAML."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"Could not load config: {e}")
            return {}
    
    def _load_prompts(self) -> Dict[str, str]:
        """Load prompt templates from prompts directory."""
        prompts_dir = Path(__file__).parent / "prompts"
        prompts = {}
        
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob("*.txt"):
                prompt_name = prompt_file.stem
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompts[prompt_name] = f.read()
        
        return prompts
    
    def _load_tools_map(self) -> Dict[str, Any]:
        """Load tools mapping from tools_map.yaml."""
        tools_map_path = Path(__file__).parent / "tools_map.yaml"
        
        try:
            with open(tools_map_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.warning(f"Could not load tools_map: {e}")
            return {}
    
    def analyze_product(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze product information and assess market potential.
        
        Args:
            product_info: Dictionary containing product details
            
        Returns:
            Dictionary with analysis results
        """
        self.logger.info("Starting product analysis", agent_id=self.agent_id)
        
        # Store product info in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="product_info",
            value=product_info,
            memory_type="short_term"
        )
        
        # Simulate strategic analysis
        analysis = {
            "product_name": product_info.get("name", "Unknown Product"),
            "category": product_info.get("category", "General"),
            "target_audience": self._identify_target_audience(product_info),
            "unique_selling_points": self._extract_usps(product_info),
            "competitive_advantages": self._assess_advantages(product_info),
            "market_potential": "High",
            "recommended_strategy": "Multi-channel aggressive launch",
            "priority_channels": ["Amazon", "Facebook", "Instagram", "TikTok"],
            "budget_allocation": {
                "amazon_ppc": 40,
                "social_media": 35,
                "content_creation": 15,
                "influencer": 10
            }
        }
        
        # Store analysis in memory
        self.memory.store(
            agent_id=self.agent_id,
            key="product_analysis",
            value=analysis,
            memory_type="long_term"
        )
        
        self.logger.success("Product analysis completed", agent_id=self.agent_id)
        return analysis
    
    def create_strategic_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create comprehensive strategic plan based on analysis.
        
        Args:
            analysis: Product analysis results
            
        Returns:
            Strategic plan dictionary
        """
        self.logger.info("Creating strategic plan", agent_id=self.agent_id)
        
        plan = {
            "campaign_name": f"{analysis['product_name']} Launch Campaign 2025",
            "objectives": [
                "Achieve 1000+ units sold in first month",
                "Reach #1 BSR in category",
                "Generate 100+ verified reviews",
                "Build social media following of 10k+"
            ],
            "timeline": {
                "phase_1_research": "Days 1-3",
                "phase_2_content": "Days 4-7",
                "phase_3_launch": "Days 8-14",
                "phase_4_optimize": "Days 15-30"
            },
            "success_metrics": {
                "primary": ["Sales volume", "BSR ranking", "Conversion rate"],
                "secondary": ["Review velocity", "Social engagement", "Traffic"]
            },
            "risk_factors": [
                "High competition in category",
                "Seasonal demand fluctuations",
                "Potential review velocity restrictions"
            ],
            "mitigation_strategies": [
                "Diversify traffic sources",
                "Build email list early",
                "Focus on organic ranking"
            ]
        }
        
        # Store plan in shared memory
        self.memory.share_memory(
            source_agent=self.agent_id,
            target_agent="all",
            key="strategic_plan",
            value=plan
        )
        
        self.logger.success("Strategic plan created", agent_id=self.agent_id)
        return plan
    
    def coordinate_workflow(self, workflow_stage: str) -> Dict[str, Any]:
        """
        Coordinate workflow and assign tasks to other agents.
        
        Args:
            workflow_stage: Current stage of workflow
            
        Returns:
            Coordination instructions
        """
        self.logger.info(f"Coordinating workflow: {workflow_stage}", agent_id=self.agent_id)
        
        coordination = {
            "stage": workflow_stage,
            "instructions": {},
            "dependencies": {},
            "expected_outputs": {}
        }
        
        if workflow_stage == "research":
            coordination["instructions"] = {
                "market_research_analyst": "Analyze competitors and market trends",
                "seo_specialist": "Research keywords and optimization opportunities"
            }
            coordination["dependencies"] = {
                "market_research_analyst": [],
                "seo_specialist": []
            }
            coordination["expected_outputs"] = {
                "market_research_analyst": "competitor_analysis",
                "seo_specialist": "keyword_strategy"
            }
        
        elif workflow_stage == "content_creation":
            coordination["instructions"] = {
                "copywriter": "Create Amazon listing with title, bullets, description"
            }
            coordination["dependencies"] = {
                "copywriter": ["market_research_analyst", "seo_specialist"]
            }
            coordination["expected_outputs"] = {
                "copywriter": "amazon_listing"
            }
        
        elif workflow_stage == "social_campaign":
            coordination["instructions"] = {
                "social_media_marketer": "Design multi-platform social campaigns"
            }
            coordination["dependencies"] = {
                "social_media_marketer": ["copywriter"]
            }
            coordination["expected_outputs"] = {
                "social_media_marketer": "social_campaigns"
            }
        
        elif workflow_stage == "validation":
            coordination["instructions"] = {
                "quality_validator": "Validate all content for compliance and quality"
            }
            coordination["dependencies"] = {
                "quality_validator": ["copywriter", "social_media_marketer"]
            }
            coordination["expected_outputs"] = {
                "quality_validator": "validation_report"
            }
        
        # Store coordination in memory
        self.memory.store(
            agent_id=self.agent_id,
            key=f"coordination_{workflow_stage}",
            value=coordination,
            memory_type="working"
        )
        
        return coordination
    
    def _identify_target_audience(self, product_info: Dict[str, Any]) -> str:
        """Identify target audience based on product information."""
        category = product_info.get("category", "").lower()
        
        audience_map = {
            "electronics": "Tech-savvy consumers, ages 25-45",
            "home": "Homeowners and renters, ages 30-55",
            "beauty": "Beauty enthusiasts, ages 18-40",
            "fitness": "Health-conscious individuals, ages 20-50",
            "kitchen": "Home cooks and food enthusiasts, ages 25-60"
        }
        
        for key, audience in audience_map.items():
            if key in category:
                return audience
        
        return "General consumers, ages 25-50"
    
    def _extract_usps(self, product_info: Dict[str, Any]) -> list:
        """Extract unique selling points from product information."""
        features = product_info.get("features", [])
        
        if isinstance(features, list) and features:
            return features[:3]  # Top 3 features
        
        return [
            "High-quality materials",
            "Innovative design",
            "Excellent value for money"
        ]
    
    def _assess_advantages(self, product_info: Dict[str, Any]) -> list:
        """Assess competitive advantages."""
        return [
            "Premium quality at competitive price",
            "Strong brand reputation",
            "Excellent customer reviews",
            "Fast shipping options"
        ]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and memory state."""
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "status": "active",
            "memory_keys": list(self.memory.retrieve(self.agent_id, "all", "short_term").keys()),
            "tools_available": list(self.tools_map.keys()) if self.tools_map else []
        }
