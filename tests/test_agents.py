"""
Agent Tests - Unit tests for all agent implementations

Tests agent initialization, configuration loading, and core functionality.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.lead_planner.agent import LeadPlannerAgent
from agents.market_research_analyst.agent import MarketResearchAnalystAgent
from agents.seo_specialist.agent import SEOSpecialistAgent
from agents.copywriter.agent import CopywriterAgent
from agents.social_media_marketer.agent import SocialMediaMarketerAgent
from agents.quality_validator.agent import QualityValidatorAgent

from shared.memory_manager import MemoryManager
from shared.logger import Logger


class TestLeadPlannerAgent(unittest.TestCase):
    """Test Lead Planner Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.memory = MemoryManager()
        self.logger = Logger()
        self.agent = LeadPlannerAgent(
            memory_manager=self.memory,
            logger=self.logger
        )
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertEqual(self.agent.agent_id, "lead_planner")
        self.assertIsNotNone(self.agent.config)
        self.assertIsNotNone(self.agent.memory)
    
    def test_product_analysis(self):
        """Test product analysis functionality"""
        product_info = {
            "name": "Test Product",
            "category": "Electronics",
            "features": ["Feature 1", "Feature 2"]
        }
        
        result = self.agent.analyze_product(product_info)
        
        self.assertIn("product_name", result)
        self.assertIn("target_audience", result)
        self.assertIn("market_potential", result)
    
    def test_strategic_plan_creation(self):
        """Test strategic plan generation"""
        analysis = {
            "product_name": "Test Product",
            "category": "Electronics"
        }
        
        plan = self.agent.create_strategic_plan(analysis)
        
        self.assertIn("campaign_name", plan)
        self.assertIn("objectives", plan)
        self.assertIn("timeline", plan)


class TestMarketResearchAgent(unittest.TestCase):
    """Test Market Research Analyst Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.memory = MemoryManager()
        self.logger = Logger()
        self.agent = MarketResearchAnalystAgent(
            memory_manager=self.memory,
            logger=self.logger
        )
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertEqual(self.agent.agent_id, "market_research_analyst")
        self.assertIsNotNone(self.agent.web_search)
    
    def test_market_analysis(self):
        """Test market analysis functionality"""
        product_info = {
            "name": "Test Product",
            "category": "Electronics"
        }
        
        result = self.agent.analyze_market(product_info)
        
        self.assertIn("market_size", result)
        self.assertIn("trends", result)
        self.assertIn("opportunities", result)


class TestSEOSpecialistAgent(unittest.TestCase):
    """Test SEO Specialist Agent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.memory = MemoryManager()
        self.logger = Logger()
        self.agent = SEOSpecialistAgent(
            memory_manager=self.memory,
            logger=self.logger
        )
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertEqual(self.agent.agent_id, "seo_specialist")
        self.assertIsNotNone(self.agent.keyword_tool)
    
    def test_keyword_research(self):
        """Test keyword research functionality"""
        product_info = {
            "name": "Water Bottle",
            "category": "Kitchen"
        }
        
        result = self.agent.research_keywords(product_info)
        
        self.assertIn("primary_keywords", result)
        self.assertIn("secondary_keywords", result)
        self.assertIn("long_tail_keywords", result)


class TestAllAgents(unittest.TestCase):
    """Test all agents can be instantiated"""
    
    def test_all_agents_initialize(self):
        """Test that all 6 agents can be created"""
        memory = MemoryManager()
        logger = Logger()
        
        agents = [
            LeadPlannerAgent(memory_manager=memory, logger=logger),
            MarketResearchAnalystAgent(memory_manager=memory, logger=logger),
            SEOSpecialistAgent(memory_manager=memory, logger=logger),
            CopywriterAgent(memory_manager=memory, logger=logger),
            SocialMediaMarketerAgent(memory_manager=memory, logger=logger),
            QualityValidatorAgent(memory_manager=memory, logger=logger)
        ]
        
        self.assertEqual(len(agents), 6)
        
        for agent in agents:
            self.assertIsNotNone(agent.agent_id)
            self.assertIsNotNone(agent.memory)
            self.assertIsNotNone(agent.logger)


if __name__ == "__main__":
    unittest.main()
