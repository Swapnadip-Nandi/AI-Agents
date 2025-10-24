"""
Monitor for ADK Multi-Agent System
Tracks agent execution, performance metrics, and workflow progress.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path


class AgentMonitor:
    """
    Monitors individual agent execution and performance.
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        """
        Initialize agent monitor.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent name
        """
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.tool_calls: List[Dict] = []
        self.errors: List[Dict] = []
        self.metrics: Dict[str, Any] = {
            "token_usage": 0,
            "api_calls": 0,
            "tool_invocations": 0,
            "retry_count": 0
        }
        
    def start(self):
        """Mark agent execution start."""
        self.start_time = datetime.now()
        
    def end(self):
        """Mark agent execution end."""
        self.end_time = datetime.now()
        
    def log_tool_call(self, tool_name: str, duration: float, success: bool):
        """
        Log a tool invocation.
        
        Args:
            tool_name: Name of the tool
            duration: Execution time in seconds
            success: Whether the call succeeded
        """
        self.tool_calls.append({
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "success": success
        })
        self.metrics["tool_invocations"] += 1
        
    def log_error(self, error: Exception, context: Optional[str] = None):
        """
        Log an error.
        
        Args:
            error: Exception object
            context: Optional context information
        """
        self.errors.append({
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        
    def increment_metric(self, metric_name: str, value: int = 1):
        """
        Increment a metric counter.
        
        Args:
            metric_name: Name of the metric
            value: Amount to increment
        """
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
        else:
            self.metrics[metric_name] = value
            
    def get_execution_time(self) -> float:
        """Get total execution time in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
        
    def get_summary(self) -> Dict[str, Any]:
        """
        Get execution summary.
        
        Returns:
            Summary dictionary
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "execution_time": self.get_execution_time(),
            "started_at": self.start_time.isoformat() if self.start_time else None,
            "ended_at": self.end_time.isoformat() if self.end_time else None,
            "metrics": self.metrics,
            "tool_calls_count": len(self.tool_calls),
            "error_count": len(self.errors),
            "success": len(self.errors) == 0
        }


class WorkflowMonitor:
    """
    Monitors entire workflow execution with all agents.
    """
    
    def __init__(self, workflow_id: str):
        """
        Initialize workflow monitor.
        
        Args:
            workflow_id: Unique workflow identifier
        """
        self.workflow_id = workflow_id
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.agent_monitors: Dict[str, AgentMonitor] = {}
        self.stage_timings: Dict[str, Dict] = {}
        self.events: List[Dict] = []
        self.parallel_executions: List[Dict] = []
        
    def start(self):
        """Start workflow monitoring."""
        self.start_time = datetime.now()
        self._log_event("workflow_started", {"workflow_id": self.workflow_id})
        
    def end(self):
        """End workflow monitoring."""
        self.end_time = datetime.now()
        self._log_event("workflow_completed", {"workflow_id": self.workflow_id})
        
    def register_agent(self, agent_id: str, agent_name: str) -> AgentMonitor:
        """
        Register an agent for monitoring.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent name
            
        Returns:
            AgentMonitor instance
        """
        monitor = AgentMonitor(agent_id, agent_name)
        self.agent_monitors[agent_id] = monitor
        return monitor
        
    def start_stage(self, stage_id: str, stage_name: str):
        """
        Mark stage execution start.
        
        Args:
            stage_id: Stage identifier
            stage_name: Stage name
        """
        self.stage_timings[stage_id] = {
            "name": stage_name,
            "start_time": datetime.now(),
            "end_time": None
        }
        self._log_event("stage_started", {
            "stage_id": stage_id,
            "stage_name": stage_name
        })
        
    def end_stage(self, stage_id: str):
        """
        Mark stage execution end.
        
        Args:
            stage_id: Stage identifier
        """
        if stage_id in self.stage_timings:
            self.stage_timings[stage_id]["end_time"] = datetime.now()
            self._log_event("stage_completed", {"stage_id": stage_id})
            
    def log_parallel_execution(self, agent_ids: List[str], duration: float):
        """
        Log parallel agent execution.
        
        Args:
            agent_ids: List of agents that ran in parallel
            duration: Total execution time
        """
        self.parallel_executions.append({
            "agents": agent_ids,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
        self._log_event("parallel_execution", {
            "agent_count": len(agent_ids),
            "duration": duration
        })
        
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """
        Log a workflow event.
        
        Args:
            event_type: Type of event
            data: Event data
        """
        self.events.append({
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        
    def get_total_execution_time(self) -> float:
        """Get total workflow execution time in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
        
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics summary.
        
        Returns:
            Metrics dictionary
        """
        # Aggregate agent metrics
        total_tokens = sum(m.metrics["token_usage"] for m in self.agent_monitors.values())
        total_api_calls = sum(m.metrics["api_calls"] for m in self.agent_monitors.values())
        total_tool_calls = sum(m.metrics["tool_invocations"] for m in self.agent_monitors.values())
        total_errors = sum(len(m.errors) for m in self.agent_monitors.values())
        
        # Calculate stage durations
        stage_durations = {}
        for stage_id, timing in self.stage_timings.items():
            if timing["end_time"]:
                duration = (timing["end_time"] - timing["start_time"]).total_seconds()
                stage_durations[stage_id] = {
                    "name": timing["name"],
                    "duration": duration
                }
        
        return {
            "workflow_id": self.workflow_id,
            "total_execution_time": self.get_total_execution_time(),
            "started_at": self.start_time.isoformat() if self.start_time else None,
            "ended_at": self.end_time.isoformat() if self.end_time else None,
            "agents_executed": len(self.agent_monitors),
            "stages_completed": len([t for t in self.stage_timings.values() if t["end_time"]]),
            "parallel_executions": len(self.parallel_executions),
            "total_tokens_used": total_tokens,
            "total_api_calls": total_api_calls,
            "total_tool_calls": total_tool_calls,
            "total_errors": total_errors,
            "stage_durations": stage_durations,
            "success": total_errors == 0
        }
        
    def get_agent_performance(self) -> List[Dict[str, Any]]:
        """
        Get performance summary for all agents.
        
        Returns:
            List of agent summaries
        """
        return [monitor.get_summary() for monitor in self.agent_monitors.values()]
        
    def export_report(self, output_path: str):
        """
        Export monitoring report to JSON file.
        
        Args:
            output_path: Path to save the report
        """
        report = {
            "workflow_summary": self.get_metrics_summary(),
            "agent_performance": self.get_agent_performance(),
            "events": self.events,
            "parallel_executions": self.parallel_executions
        }
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            print(f"Error exporting monitoring report: {e}")
            
    def get_performance_insights(self) -> Dict[str, Any]:
        """
        Get performance insights and recommendations.
        
        Returns:
            Insights dictionary
        """
        metrics = self.get_metrics_summary()
        agent_perf = self.get_agent_performance()
        
        # Find slowest agent
        slowest_agent = max(agent_perf, key=lambda x: x["execution_time"]) if agent_perf else None
        
        # Find agent with most errors
        most_errors = max(agent_perf, key=lambda x: x["error_count"]) if agent_perf else None
        
        # Calculate efficiency
        total_time = metrics["total_execution_time"]
        parallel_time_saved = sum(p["duration"] for p in self.parallel_executions)
        
        insights = {
            "overall_status": "success" if metrics["success"] else "failed",
            "execution_efficiency": "good" if total_time < 120 else "needs_optimization",
            "slowest_agent": slowest_agent["agent_name"] if slowest_agent else None,
            "agent_with_most_errors": most_errors["agent_name"] if most_errors and most_errors["error_count"] > 0 else None,
            "parallel_time_saved": parallel_time_saved,
            "recommendations": []
        }
        
        # Add recommendations
        if total_time > 180:
            insights["recommendations"].append("Consider increasing parallel execution")
        if metrics["total_errors"] > 0:
            insights["recommendations"].append("Review error logs and implement retry logic")
        if metrics["total_tokens_used"] > 50000:
            insights["recommendations"].append("Optimize prompts to reduce token usage")
            
        return insights
