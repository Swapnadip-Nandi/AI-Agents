"""
Unit tests for Amazon Campaign Multi-Agent System
"""

import sys
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.web_search_tool import WebSearchTool
from tools.keyword_research_tool import KeywordResearchTool
from tools.amazon_listing_parser import AmazonListingParser
from tools.compliance_checker import ComplianceChecker
from tools.calculator_tool import CalculatorTool
from tools.file_parser_tool import FileParserTool

from shared.memory_manager import MemoryManager
from shared.context_manager import ContextManager
from shared.state_tracker import StateTracker, TaskStatus
from shared.hallucination_guard import HallucinationGuard


class TestTools:
    """Test all tools functionality."""
    
    def test_web_search_tool(self):
        """Test web search tool."""
        tool = WebSearchTool(max_results=3)
        results = tool.search("amazon marketplace")
        
        assert len(results) > 0
        assert all("title" in r for r in results)
        assert all("snippet" in r for r in results)
        
    def test_keyword_research_tool(self):
        """Test keyword research tool."""
        tool = KeywordResearchTool()
        keywords = tool.generate_keywords("bluetooth headphones", "electronics")
        
        assert len(keywords) > 0
        assert all("keyword" in k for k in keywords)
        assert all("search_volume" in k for k in keywords)
        assert all("competition" in k for k in keywords)
        
    def test_amazon_listing_parser(self):
        """Test Amazon listing parser."""
        parser = AmazonListingParser()
        
        # Test title validation
        title = "Premium Bluetooth Headphones - Noise Cancelling Wireless"
        validation = parser.validate_title(title)
        
        assert "valid" in validation
        assert "score" in validation
        assert validation["length"] == len(title)
        
    def test_compliance_checker(self):
        """Test compliance checker."""
        checker = ComplianceChecker()
        
        # Test compliant content
        content = "High quality bluetooth headphones with noise cancellation"
        result = checker.check_compliance(content, "title")
        
        assert "compliant" in result
        assert "score" in result
        assert "violations" in result
        
    def test_calculator_tool(self):
        """Test calculator tool."""
        calc = CalculatorTool()
        
        # Test basic calculation
        result = calc.calculate("10 + 5")
        assert result == 15.0
        
        # Test percentage
        percent = calc.percentage(100, 20)
        assert percent == 20.0
        
        # Test ROI
        roi = calc.roi(50, 100)
        assert roi == 50.0
        
    def test_file_parser_tool(self):
        """Test file parser tool."""
        parser = FileParserTool()
        
        # Test supported formats
        assert '.json' in parser.supported_formats
        assert '.csv' in parser.supported_formats
        assert '.txt' in parser.supported_formats


class TestSharedUtilities:
    """Test shared utility classes."""
    
    def test_memory_manager(self):
        """Test memory manager."""
        manager = MemoryManager()
        
        # Test store and retrieve
        agent_id = "test_agent"
        key = "test_key"
        value = {"data": "test_value"}
        
        success = manager.store(agent_id, key, value, "short_term")
        assert success is True
        
        retrieved = manager.retrieve(agent_id, key, "short_term")
        assert retrieved == value
        
    def test_context_manager(self):
        """Test context manager."""
        workflow_config = {"data_flow": {"context_propagation": []}}
        manager = ContextManager(workflow_config)
        
        # Test context initialization
        input_data = {
            "product_info": {"product_name": "Test Product"},
            "campaign_params": {"budget": "$1000"}
        }
        
        context = manager.initialize_workflow_context(input_data)
        
        assert "workflow_id" in context
        assert "product_info" in context
        assert context["product_info"]["product_name"] == "Test Product"
        
    def test_state_tracker(self):
        """Test state tracker."""
        tracker = StateTracker("test_workflow")
        
        # Register and execute task
        tracker.register_task("task_1", "Test Task", [])
        tracker.start_task("task_1")
        tracker.complete_task("task_1", {"result": "success"})
        
        # Check status
        status = tracker.get_task_status("task_1")
        assert status == TaskStatus.COMPLETED
        
        result = tracker.get_task_result("task_1")
        assert result == {"result": "success"}
        
    def test_hallucination_guard(self):
        """Test hallucination guard."""
        guard = HallucinationGuard()
        
        # Test content validation
        content = {
            "product_name": "Test Product",
            "description": "High quality product"
        }
        
        context = {
            "product_info": {"product_name": "Test Product"}
        }
        
        is_valid, report = guard.validate_content(content, context)
        
        assert "score" in report
        assert "violations" in report
        assert "warnings" in report


class TestIntegration:
    """Integration tests."""
    
    def test_workflow_memory_integration(self):
        """Test workflow with memory integration."""
        memory = MemoryManager()
        workflow_config = {"data_flow": {"context_propagation": []}}
        context_mgr = ContextManager(workflow_config)
        
        # Simulate workflow
        input_data = {"product_info": {"product_name": "Test Product"}}
        context = context_mgr.initialize_workflow_context(input_data)
        
        # Agent stores data
        memory.store("agent_1", "result", {"data": "test"}, "shared")
        
        # Another agent retrieves
        retrieved = memory.retrieve("agent_1", "result", "shared")
        assert retrieved == {"data": "test"}
        
    def test_tool_chain(self):
        """Test chaining multiple tools."""
        # Research keywords
        kw_tool = KeywordResearchTool()
        keywords = kw_tool.generate_keywords("headphones", "electronics")
        
        # Create listing
        parser = AmazonListingParser()
        title = f"{keywords[0]['keyword']} - Premium Quality"
        validation = parser.validate_title(title)
        
        # Check compliance
        checker = ComplianceChecker()
        compliance = checker.check_compliance(title, "title")
        
        assert validation["valid"] is not None
        assert compliance["compliant"] is not None


def run_tests():
    """Run all tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_tests()
