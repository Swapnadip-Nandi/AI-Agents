"""
Campaign Workflow - Main Sequential Orchestration

This workflow orchestrates the entire campaign creation process through all agents.
"""

import os
import time
from typing import Dict, Any, Optional
from pathlib import Path

from shared.memory_manager import MemoryManager
from shared.context_manager import ContextManager
from shared.logger import Logger
from shared.monitor import WorkflowMonitor
from shared.state_tracker import StateTracker

from agents.lead_planner.agent import LeadPlannerAgent
from agents.market_research_analyst.agent import MarketResearchAnalystAgent
from agents.seo_specialist.agent import SEOSpecialistAgent
from agents.copywriter.agent import CopywriterAgent
from agents.social_media_marketer.agent import SocialMediaMarketerAgent
from agents.quality_validator.agent import QualityValidatorAgent

from .parallel_research_workflow import ParallelResearchWorkflow
from .structured_output import StructuredOutputGenerator
from .monitor_workflow import WorkflowEventMonitor


class CampaignWorkflow:
    """
    Main Campaign Workflow - Sequential orchestration with parallel stages
    
    Workflow Stages:
    1. Strategic Planning (Lead Planner)
    2. Research (Market Research + SEO in parallel)
    3. Content Creation (Copywriter)
    4. Social Campaigns (Social Media Marketer)
    5. Quality Validation (Quality Validator)
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        memory_manager: Optional[MemoryManager] = None,
        logger: Optional[Logger] = None
    ):
        """Initialize the campaign workflow."""
        self.logger = logger or Logger()
        self.memory = memory_manager or MemoryManager()
        self.context = ContextManager(workflow_config={})
        self.monitor = WorkflowMonitor(workflow_id="campaign_workflow")
        self.state_tracker = StateTracker(workflow_id="campaign_workflow")
        self.event_monitor = WorkflowEventMonitor(self.logger)
        
        # Initialize all agents with shared resources
        self.logger.info("Initializing campaign workflow agents")
        
        self.lead_planner = LeadPlannerAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        self.market_researcher = MarketResearchAnalystAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        self.seo_specialist = SEOSpecialistAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        self.copywriter = CopywriterAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        self.social_marketer = SocialMediaMarketerAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        self.quality_validator = QualityValidatorAgent(
            memory_manager=self.memory,
            context_manager=self.context,
            logger=self.logger
        )
        
        # Initialize parallel research workflow
        self.parallel_research = ParallelResearchWorkflow(
            market_researcher=self.market_researcher,
            seo_specialist=self.seo_specialist,
            logger=self.logger
        )
        
        # Initialize output generator
        self.output_generator = StructuredOutputGenerator(
            memory_manager=self.memory,
            logger=self.logger
        )
        
        self.logger.success("Campaign workflow initialized")
    
    def execute(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete campaign workflow.
        
        Args:
            product_info: Product information to create campaign for
            
        Returns:
            Complete campaign results
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING AMAZON CAMPAIGN WORKFLOW")
        self.logger.info("=" * 80)
        
        workflow_start = time.time()
        
        try:
            # Stage 1: Strategic Planning
            self.logger.info("\n[STAGE 1/5] Strategic Planning")
            stage1_start = time.time()
            
            self.state_tracker.update_task_status("strategic_planning", "in_progress")
            self.event_monitor.log_stage_start("Strategic Planning", 1)
            
            analysis = self.lead_planner.analyze_product(product_info)
            strategic_plan = self.lead_planner.create_strategic_plan(analysis)
            coordination = self.lead_planner.coordinate_workflow("research")
            
            self.state_tracker.update_task_status("strategic_planning", "completed")
            self.monitor.track_agent_execution(
                agent_id="lead_planner",
                duration=time.time() - stage1_start,
                success=True
            )
            self.event_monitor.log_stage_end("Strategic Planning", 1, time.time() - stage1_start)
            
            # Stage 2: Parallel Research (Market Research + SEO)
            self.logger.info("\n[STAGE 2/5] Research Phase (Parallel Execution)")
            stage2_start = time.time()
            
            self.state_tracker.update_task_status("research", "in_progress")
            self.event_monitor.log_stage_start("Research Phase", 2)
            
            research_results = self.parallel_research.execute(product_info)
            
            self.state_tracker.update_task_status("research", "completed")
            self.monitor.track_workflow_stage(
                stage="research",
                duration=time.time() - stage2_start,
                agents_involved=["market_research_analyst", "seo_specialist"]
            )
            self.event_monitor.log_stage_end("Research Phase", 2, time.time() - stage2_start)
            
            # Stage 3: Content Creation
            self.logger.info("\n[STAGE 3/5] Content Creation")
            stage3_start = time.time()
            
            self.state_tracker.update_task_status("content_creation", "in_progress")
            self.event_monitor.log_stage_start("Content Creation", 3)
            
            listing = self.copywriter.create_amazon_listing(product_info)
            
            self.state_tracker.update_task_status("content_creation", "completed")
            self.monitor.track_agent_execution(
                agent_id="copywriter",
                duration=time.time() - stage3_start,
                success=True
            )
            self.event_monitor.log_stage_end("Content Creation", 3, time.time() - stage3_start)
            
            # Stage 4: Social Media Campaigns
            self.logger.info("\n[STAGE 4/5] Social Media Campaign Design")
            stage4_start = time.time()
            
            self.state_tracker.update_task_status("social_campaigns", "in_progress")
            self.event_monitor.log_stage_start("Social Campaigns", 4)
            
            social_campaigns = self.social_marketer.create_social_campaigns(product_info)
            
            self.state_tracker.update_task_status("social_campaigns", "completed")
            self.monitor.track_agent_execution(
                agent_id="social_media_marketer",
                duration=time.time() - stage4_start,
                success=True
            )
            self.event_monitor.log_stage_end("Social Campaigns", 4, time.time() - stage4_start)
            
            # Stage 5: Quality Validation
            self.logger.info("\n[STAGE 5/5] Quality Validation")
            stage5_start = time.time()
            
            self.state_tracker.update_task_status("validation", "in_progress")
            self.event_monitor.log_stage_start("Quality Validation", 5)
            
            validation_report = self.quality_validator.validate_campaign()
            
            self.state_tracker.update_task_status("validation", "completed")
            self.monitor.track_agent_execution(
                agent_id="quality_validator",
                duration=time.time() - stage5_start,
                success=True
            )
            self.event_monitor.log_stage_end("Quality Validation", 5, time.time() - stage5_start)
            
            # Generate structured outputs
            self.logger.info("\n[OUTPUT GENERATION] Creating structured outputs")
            
            campaign_results = {
                "product_info": product_info,
                "strategic_plan": strategic_plan,
                "market_analysis": research_results["market_analysis"],
                "keyword_research": research_results["keyword_research"],
                "amazon_listing": listing,
                "social_campaigns": social_campaigns,
                "validation_report": validation_report,
                "workflow_metrics": self.monitor.get_metrics(),
                "execution_timeline": self.state_tracker.get_execution_summary()
            }
            
            # Generate JSON and Markdown outputs
            outputs = self.output_generator.generate_outputs(campaign_results)
            
            workflow_duration = time.time() - workflow_start
            
            self.logger.info("\n" + "=" * 80)
            self.logger.success(f"WORKFLOW COMPLETED SUCCESSFULLY in {workflow_duration:.2f}s")
            self.logger.info(f"Overall Quality Score: {validation_report['overall_score']}/100")
            self.logger.info(f"Status: {validation_report['status']}")
            self.logger.info(f"Approved: {'YES' if validation_report['approval'] else 'NO'}")
            self.logger.info("=" * 80)
            
            return {
                "campaign_results": campaign_results,
                "outputs": outputs,
                "workflow_duration": workflow_duration,
                "approval_status": validation_report["approval"]
            }
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {str(e)}")
            self.state_tracker.update_task_status("workflow", "failed")
            raise
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            "state": self.state_tracker.get_execution_summary(),
            "metrics": self.monitor.get_metrics(),
            "agents_status": {
                "lead_planner": self.lead_planner.get_status(),
                "market_researcher": self.market_researcher.get_status(),
                "seo_specialist": self.seo_specialist.get_status(),
                "copywriter": self.copywriter.get_status(),
                "social_marketer": self.social_marketer.get_status(),
                "quality_validator": self.quality_validator.get_status()
            }
        }
