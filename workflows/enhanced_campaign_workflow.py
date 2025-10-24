"""
Enhanced Campaign Workflow with Session Management, Async Logging, and Learning

Integrates:
- Session-based execution with unique IDs
- Asynchronous logging with time-series tracking
- Enhanced memory with long-term learning
- Real-time progress tracking
- Campaign template learning
"""

import os
import time
from typing import Dict, Any, Optional
from pathlib import Path

# Import new enhanced components
from shared.session_manager import SessionManager
from shared.async_logger import AsyncLogger, LogLevel, EventType
from shared.enhanced_memory import EnhancedMemoryManager
from shared.realtime_streaming import ProgressTracker, MetricsCollector
from shared.context_manager import ContextManager
from shared.state_tracker import StateTracker

# Import existing agents
from agents.lead_planner.agent import LeadPlannerAgent
from agents.market_research_analyst.agent import MarketResearchAnalystAgent
from agents.seo_specialist.agent import SEOSpecialistAgent
from agents.copywriter.agent import CopywriterAgent
from agents.social_media_marketer.agent import SocialMediaMarketerAgent
from agents.quality_validator.agent import QualityValidatorAgent

from workflows.parallel_research_workflow import ParallelResearchWorkflow
from workflows.structured_output import StructuredOutputGenerator


class EnhancedCampaignWorkflow:
    """
    Enhanced Campaign Workflow with session management and learning capabilities.
    
    New Features:
    - Unique session ID for each execution
    - Async time-series logging
    - Long-term memory with campaign learning
    - Real-time progress tracking
    - Automatic campaign template storage
    - Session-based cleanup after 7 days
    """
    
    def __init__(
        self,
        storage_root: str = "./storage",
        session_manager: Optional[SessionManager] = None
    ):
        """
        Initialize enhanced campaign workflow.
        
        Args:
            storage_root: Root storage directory
            session_manager: Optional session manager instance
        """
        self.storage_root = Path(storage_root)
        
        # Initialize session manager
        self.session_manager = session_manager or SessionManager(
            storage_root=storage_root,
            retention_days=7,
            auto_cleanup=True
        )
        
        # Session-specific components (initialized per execution)
        self.session_id: Optional[str] = None
        self.logger: Optional[AsyncLogger] = None
        self.memory: Optional[EnhancedMemoryManager] = None
        self.progress_tracker: Optional[ProgressTracker] = None
        self.metrics_collector: Optional[MetricsCollector] = None
        
        # Shared components
        self.context = ContextManager(workflow_config={})
        self.state_tracker: Optional[StateTracker] = None
    
    def execute(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete campaign workflow with session management.
        
        Args:
            product_info: Product information to create campaign for
            
        Returns:
            Complete campaign results with session information
        """
        # Create new session
        self.session_id = self.session_manager.create_session(
            product_name=product_info.get('name'),
            workflow_type="amazon_campaign"
        )
        
        session_dir = self.session_manager.get_session_dir(self.session_id)
        
        # Initialize session-specific components
        self.logger = AsyncLogger(
            session_id=self.session_id,
            session_dir=session_dir
        )
        
        self.memory = EnhancedMemoryManager(
            session_id=self.session_id,
            session_dir=session_dir,
            storage_root=self.storage_root,
            enable_caching=True
        )
        
        self.progress_tracker = ProgressTracker(session_id=self.session_id)
        self.metrics_collector = MetricsCollector(session_id=self.session_id)
        self.state_tracker = StateTracker(workflow_id=self.session_id)
        
        # Log session start
        self.logger.log(
            EventType.SESSION_STARTED,
            LogLevel.INFO,
            f"Starting campaign workflow for: {product_info.get('name')}",
            data={
                "product_name": product_info.get('name'),
                "category": product_info.get('category'),
                "session_id": self.session_id
            }
        )
        
        self.metrics_collector.set_start_time()
        workflow_start = time.time()
        
        try:
            # Check for similar past campaigns (Learning Feature)
            suggestions = self.memory.get_learning_suggestions(product_info)
            
            if suggestions and suggestions.get('found_similar_campaign'):
                self.logger.info(
                    f"💡 {suggestions['message']}",
                    data=suggestions
                )
                print(f"\n{'='*80}")
                print(f"💡 LEARNING FROM PAST CAMPAIGNS")
                print(f"{'='*80}")
                print(f"Found similar campaign: {suggestions['reference_campaign']['product_name']}")
                print(f"Quality Score: {suggestions['reference_campaign']['quality_score']}%")
                print(f"Similarity: {suggestions['similarity_score']*100:.1f}%")
                print(f"Consider using suggested keywords and structure as reference.")
                print(f"{'='*80}\n")
            
            # Initialize all agents with enhanced components
            agents = self._initialize_agents()
            
            # Stage 1: Strategic Planning
            print(f"\n[STAGE 1/6] Strategic Planning")
            self.progress_tracker.update_stage(0, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="lead_planner",
                agent_name="Lead Planner",
                task="Strategic planning and campaign architecture"
            )
            
            analysis = agents['lead_planner'].analyze_product(product_info)
            strategic_plan = agents['lead_planner'].create_strategic_plan(analysis)
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="lead_planner",
                agent_name="Lead Planner",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("lead_planner", stage_duration)
            self.progress_tracker.update_stage(0, 100)
            
            # Stage 2: Market Research
            print(f"\n[STAGE 2/6] Market Research")
            self.progress_tracker.update_stage(1, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="market_research_analyst",
                agent_name="Market Research Analyst",
                task="Competitive analysis and market intelligence"
            )
            
            market_analysis = agents['market_researcher'].analyze_market(product_info)
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="market_research_analyst",
                agent_name="Market Research Analyst",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("market_research_analyst", stage_duration)
            self.progress_tracker.update_stage(1, 100)
            
            # Stage 3: SEO Analysis
            print(f"\n[STAGE 3/6] SEO Keyword Research")
            self.progress_tracker.update_stage(2, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="seo_specialist",
                agent_name="SEO Specialist",
                task="Keyword research and optimization"
            )
            
            keyword_research = agents['seo_specialist'].research_keywords(product_info)
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="seo_specialist",
                agent_name="SEO Specialist",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("seo_specialist", stage_duration)
            self.progress_tracker.update_stage(2, 100)
            
            # Stage 4: Content Creation
            print(f"\n[STAGE 4/6] Content Creation")
            self.progress_tracker.update_stage(3, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="copywriter",
                agent_name="Copywriter",
                task="Amazon listing creation"
            )
            
            listing = agents['copywriter'].create_amazon_listing(product_info)
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="copywriter",
                agent_name="Copywriter",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("copywriter", stage_duration)
            self.progress_tracker.update_stage(3, 100)
            
            # Stage 5: Social Media Campaigns
            print(f"\n[STAGE 5/6] Social Media Campaign Design")
            self.progress_tracker.update_stage(4, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="social_media_marketer",
                agent_name="Social Media Marketer",
                task="Multi-platform campaign design"
            )
            
            social_campaigns = agents['social_marketer'].create_social_campaigns(product_info)
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="social_media_marketer",
                agent_name="Social Media Marketer",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("social_media_marketer", stage_duration)
            self.progress_tracker.update_stage(4, 100)
            
            # Stage 6: Quality Validation
            print(f"\n[STAGE 6/6] Quality Validation")
            self.progress_tracker.update_stage(5, 0)
            stage_start = time.time()
            
            event_id = self.logger.agent_started(
                agent_id="quality_validator",
                agent_name="Quality Validator",
                task="Compliance checking and quality assurance"
            )
            
            validation_report = agents['quality_validator'].validate_campaign()
            
            stage_duration = (time.time() - stage_start) * 1000
            self.logger.agent_completed(
                agent_id="quality_validator",
                agent_name="Quality Validator",
                duration_ms=stage_duration,
                parent_event_id=event_id
            )
            self.metrics_collector.record_agent_execution("quality_validator", stage_duration)
            self.progress_tracker.update_stage(5, 100)
            
            # Save campaign as template if high quality (>= 85%)
            if validation_report.get('overall_score', 0) >= 85:
                template_id = self.memory.save_campaign_template(
                    product_name=product_info.get('name', 'Unknown'),
                    category=product_info.get('category', 'General'),
                    quality_score=validation_report['overall_score'],
                    target_audience=product_info.get('target_audience', ''),
                    keywords=keyword_research.get('primary_keywords', []),
                    listing_structure=listing,
                    social_strategy=social_campaigns,
                    success_metrics=validation_report,
                    tags=[product_info.get('category', '')]
                )
                
                self.logger.info(
                    f"📚 Campaign saved as template for future learning: {template_id}",
                    data={"template_id": template_id}
                )
            
            # Generate structured outputs
            print(f"\n[OUTPUT GENERATION] Creating structured outputs")
            
            campaign_results = {
                "session_id": self.session_id,
                "product_info": product_info,
                "strategic_plan": strategic_plan,
                "market_analysis": market_analysis,
                "keyword_research": keyword_research,
                "amazon_listing": listing,
                "social_campaigns": social_campaigns,
                "validation_report": validation_report,
                "learning_suggestions": suggestions
            }
            
            # Generate JSON and Markdown outputs
            output_generator = StructuredOutputGenerator(
                memory_manager=self.memory,
                logger=self.logger,
                output_dir=str(session_dir / "results")
            )
            
            outputs = output_generator.generate_outputs(campaign_results)
            
            # Calculate workflow duration
            workflow_duration = time.time() - workflow_start
            self.metrics_collector.set_end_time()
            
            # Update session metadata
            self.session_manager.update_session(
                session_id=self.session_id,
                status="completed",
                duration=workflow_duration,
                agent_count=6,
                quality_score=validation_report.get('overall_score')
            )
            
            # Log session completion
            self.logger.log(
                EventType.SESSION_COMPLETED,
                LogLevel.SUCCESS,
                f"Campaign workflow completed successfully in {workflow_duration:.2f}s",
                data={
                    "duration": workflow_duration,
                    "quality_score": validation_report.get('overall_score'),
                    "approval": validation_report.get('approval'),
                    "metrics": self.metrics_collector.get_metrics()
                }
            )
            
            # Display results
            print(f"\n{'='*80}")
            print(f"✅ WORKFLOW COMPLETED SUCCESSFULLY")
            print(f"{'='*80}")
            print(f"Session ID: {self.session_id}")
            print(f"Duration: {workflow_duration:.2f}s")
            print(f"Quality Score: {validation_report.get('overall_score')}/100")
            print(f"Status: {validation_report.get('status')}")
            print(f"Approved: {'YES' if validation_report.get('approval') else 'NO'}")
            print(f"\n📁 Results saved to: {session_dir / 'results'}")
            print(f"📊 Logs available at: {session_dir / 'logs'}")
            print(f"{'='*80}\n")
            
            # Stop async logger
            self.logger.stop()
            
            return {
                "session_id": self.session_id,
                "campaign_results": campaign_results,
                "outputs": outputs,
                "workflow_duration": workflow_duration,
                "approval_status": validation_report.get("approval"),
                "progress": self.progress_tracker.get_status(),
                "metrics": self.metrics_collector.get_metrics(),
                "memory_stats": self.memory.get_memory_stats()
            }
            
        except Exception as e:
            # Log error
            self.logger.error(
                f"Workflow execution failed: {str(e)}",
                data={"error": str(e), "error_type": type(e).__name__}
            )
            
            # Update session as failed
            self.session_manager.update_session(
                session_id=self.session_id,
                status="failed",
                error_count=1
            )
            
            self.metrics_collector.record_error()
            self.metrics_collector.set_end_time()
            
            # Stop async logger
            if self.logger:
                self.logger.stop()
            
            raise
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents with enhanced components."""
        return {
            'lead_planner': LeadPlannerAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            ),
            'market_researcher': MarketResearchAnalystAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            ),
            'seo_specialist': SEOSpecialistAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            ),
            'copywriter': CopywriterAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            ),
            'social_marketer': SocialMediaMarketerAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            ),
            'quality_validator': QualityValidatorAgent(
                memory_manager=self.memory,
                context_manager=self.context,
                logger=self.logger
            )
        }
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific session."""
        metadata = self.session_manager.get_session_metadata(session_id)
        if not metadata:
            return None
        
        return {
            "metadata": metadata,
            "progress": self.progress_tracker.get_status() if self.progress_tracker else None,
            "metrics": self.metrics_collector.get_metrics() if self.metrics_collector else None
        }
