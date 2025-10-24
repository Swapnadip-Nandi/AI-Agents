"""
Agents package for Amazon Campaign Multi-Agent System.

This package contains all specialized agents, each in their own directory
with dedicated configuration, prompts, tools, and memory.
"""

from .lead_planner.agent import LeadPlannerAgent
from .market_research_analyst.agent import MarketResearchAnalystAgent
from .seo_specialist.agent import SEOSpecialistAgent
from .copywriter.agent import CopywriterAgent
from .social_media_marketer.agent import SocialMediaMarketerAgent
from .quality_validator.agent import QualityValidatorAgent

# Import root agent for ADK web interface
from .agent import root_agent

__all__ = [
    "LeadPlannerAgent",
    "MarketResearchAnalystAgent",
    "SEOSpecialistAgent",
    "CopywriterAgent",
    "SocialMediaMarketerAgent",
    "QualityValidatorAgent",
    "root_agent",
]
