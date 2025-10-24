"""
Parallel Research Workflow - Execute Market Research and SEO Concurrently

This workflow demonstrates parallel execution of independent research tasks.
"""

import time
import concurrent.futures
from typing import Dict, Any
from shared.logger import Logger


class ParallelResearchWorkflow:
    """
    Parallel Research Workflow - Run Market Research and SEO simultaneously
    
    This demonstrates ADK's ability to execute independent agents in parallel
    for improved efficiency.
    """
    
    def __init__(
        self,
        market_researcher,
        seo_specialist,
        logger: Logger
    ):
        """Initialize parallel research workflow."""
        self.market_researcher = market_researcher
        self.seo_specialist = seo_specialist
        self.logger = logger
    
    def execute(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute market research and SEO analysis in parallel.
        
        Args:
            product_info: Product information
            
        Returns:
            Combined research results
        """
        self.logger.info("Starting parallel research execution...")
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both tasks
            market_future = executor.submit(
                self._run_market_research,
                product_info
            )
            
            seo_future = executor.submit(
                self._run_seo_research,
                product_info
            )
            
            # Wait for both to complete
            market_analysis = market_future.result()
            keyword_research = seo_future.result()
        
        duration = time.time() - start_time
        
        self.logger.success(
            f"Parallel research completed in {duration:.2f}s "
            f"(~50% faster than sequential)"
        )
        
        return {
            "market_analysis": market_analysis,
            "keyword_research": keyword_research,
            "execution_mode": "parallel",
            "duration": duration
        }
    
    def _run_market_research(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Run market research analysis."""
        self.logger.info("→ Running Market Research (parallel)")
        start = time.time()
        
        result = self.market_researcher.analyze_market(product_info)
        
        self.logger.info(f"  Market Research completed in {time.time() - start:.2f}s")
        return result
    
    def _run_seo_research(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """Run SEO keyword research."""
        self.logger.info("→ Running SEO Research (parallel)")
        start = time.time()
        
        result = self.seo_specialist.research_keywords(product_info)
        
        self.logger.info(f"  SEO Research completed in {time.time() - start:.2f}s")
        return result
