"""
Workflow Event Monitor - Track and Log Workflow Events

Monitors workflow execution and logs events for debugging and analytics.
"""

import time
from typing import Dict, Any, Optional
from shared.logger import Logger


class WorkflowEventMonitor:
    """Monitor workflow events and track execution metrics."""
    
    def __init__(self, logger: Logger):
        """Initialize workflow event monitor."""
        self.logger = logger
        self.events = []
        self.stage_timings = {}
    
    def log_stage_start(self, stage_name: str, stage_number: int):
        """Log workflow stage start."""
        event = {
            "type": "stage_start",
            "stage_name": stage_name,
            "stage_number": stage_number,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self.stage_timings[stage_name] = {"start": time.time()}
        
        self.logger.info(f"→ Starting Stage {stage_number}: {stage_name}")
    
    def log_stage_end(self, stage_name: str, stage_number: int, duration: float):
        """Log workflow stage completion."""
        event = {
            "type": "stage_end",
            "stage_name": stage_name,
            "stage_number": stage_number,
            "duration": duration,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        
        if stage_name in self.stage_timings:
            self.stage_timings[stage_name]["end"] = time.time()
            self.stage_timings[stage_name]["duration"] = duration
        
        self.logger.success(f"✓ Completed Stage {stage_number}: {stage_name} ({duration:.2f}s)")
    
    def log_agent_execution(
        self,
        agent_id: str,
        task: str,
        duration: Optional[float] = None,
        success: bool = True
    ):
        """Log individual agent execution."""
        event = {
            "type": "agent_execution",
            "agent_id": agent_id,
            "task": task,
            "duration": duration,
            "success": success,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        
        status = "✓" if success else "✗"
        duration_str = f"({duration:.2f}s)" if duration else ""
        self.logger.info(f"  {status} {agent_id}: {task} {duration_str}")
    
    def log_error(self, error_message: str, context: Dict[str, Any]):
        """Log workflow error."""
        event = {
            "type": "error",
            "message": error_message,
            "context": context,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        self.logger.error(f"Error: {error_message}")
    
    def get_events(self) -> list:
        """Get all logged events."""
        return self.events
    
    def get_stage_timings(self) -> Dict[str, Any]:
        """Get stage timing information."""
        return self.stage_timings
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        total_duration = 0
        if self.stage_timings:
            total_duration = sum(
                timing.get("duration", 0)
                for timing in self.stage_timings.values()
            )
        
        return {
            "total_events": len(self.events),
            "total_duration": total_duration,
            "stages_completed": len(self.stage_timings),
            "stage_timings": self.stage_timings
        }
