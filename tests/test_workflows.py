"""
Workflow Tests - Unit tests for workflow orchestration

Tests workflow execution, parallel processing, and validation loops.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.campaign_workflow import CampaignWorkflow
from workflows.parallel_research_workflow import ParallelResearchWorkflow
from workflows.validation_workflow import ValidationWorkflow

from shared.memory_manager import MemoryManager
from shared.logger import Logger


class TestCampaignWorkflow(unittest.TestCase):
    """Test Campaign Workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.memory = MemoryManager()
        self.logger = Logger()
        self.workflow = CampaignWorkflow(
            memory_manager=self.memory,
            logger=self.logger
        )
    
    def test_workflow_initialization(self):
        """Test workflow initializes correctly"""
        self.assertIsNotNone(self.workflow.lead_planner)
        self.assertIsNotNone(self.workflow.market_researcher)
        self.assertIsNotNone(self.workflow.seo_specialist)
        self.assertIsNotNone(self.workflow.copywriter)
        self.assertIsNotNone(self.workflow.social_marketer)
        self.assertIsNotNone(self.workflow.quality_validator)
    
    def test_workflow_execution(self):
        """Test workflow can execute (mock mode)"""
        product_info = {
            "name": "Test Product",
            "category": "Electronics",
            "features": ["Feature 1", "Feature 2"]
        }
        
        # This will run in simulated mode
        result = self.workflow.execute(product_info)
        
        self.assertIn("campaign_results", result)
        self.assertIn("outputs", result)
        self.assertIn("workflow_duration", result)
    
    def test_workflow_status(self):
        """Test workflow status reporting"""
        status = self.workflow.get_workflow_status()
        
        self.assertIn("state", status)
        self.assertIn("metrics", status)
        self.assertIn("agents_status", status)


class TestParallelWorkflow(unittest.TestCase):
    """Test Parallel Research Workflow"""
    
    def test_parallel_execution_concept(self):
        """Test that parallel workflow structure exists"""
        from workflows.parallel_research_workflow import ParallelResearchWorkflow
        
        # Check class exists and has expected methods
        self.assertTrue(hasattr(ParallelResearchWorkflow, 'execute'))
        self.assertTrue(hasattr(ParallelResearchWorkflow, '__init__'))


class TestValidationWorkflow(unittest.TestCase):
    """Test Validation Workflow"""
    
    def test_validation_workflow_concept(self):
        """Test that validation workflow structure exists"""
        from workflows.validation_workflow import ValidationWorkflow
        
        # Check class exists and has expected methods
        self.assertTrue(hasattr(ValidationWorkflow, 'execute'))
        self.assertTrue(hasattr(ValidationWorkflow, '__init__'))


if __name__ == "__main__":
    unittest.main()
