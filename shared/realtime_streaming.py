"""
Real-Time Log Streaming for ADK Web Interface

Provides Server-Sent Events (SSE) for real-time log streaming to web UI.
Follows Google ADK patterns for event monitoring.

Features:
- Server-Sent Events (SSE) for real-time updates
- Session-based log filtering
- Event type filtering
- Agent-specific log streaming
- Buffered streaming with backpressure handling
"""

import json
import time
from pathlib import Path
from typing import Optional, Generator, Dict, Any
from datetime import datetime
import threading


class LogStreamer:
    """
    Real-time log streaming using Server-Sent Events (SSE).
    
    Monitors log files and streams new entries to connected clients.
    """
    
    def __init__(self, session_dir: Path):
        """
        Initialize log streamer.
        
        Args:
            session_dir: Session directory containing logs
        """
        self.session_dir = Path(session_dir)
        self.logs_dir = self.session_dir / "logs"
        self.master_log = self.logs_dir / "session_timeseries.jsonl"
        
        # Track file positions for tailing
        self.file_positions: Dict[str, int] = {}
        self._lock = threading.Lock()
    
    def stream_logs(
        self,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        level: Optional[str] = None,
        follow: bool = True
    ) -> Generator[str, None, None]:
        """
        Stream logs in Server-Sent Events format.
        
        Args:
            agent_id: Filter by agent ID
            event_type: Filter by event type
            level: Filter by log level
            follow: Continue streaming new events (tail -f mode)
            
        Yields:
            SSE formatted messages
        """
        # Determine which log file to stream
        if agent_id:
            log_file = self.logs_dir / f"agent_{agent_id}.jsonl"
        else:
            log_file = self.master_log
        
        if not log_file.exists():
            yield self._format_sse("error", {"message": "Log file not found"})
            return
        
        # Initialize file position
        with self._lock:
            if str(log_file) not in self.file_positions:
                self.file_positions[str(log_file)] = 0
        
        # Stream existing logs
        with open(log_file, 'r', encoding='utf-8') as f:
            # Seek to last position
            f.seek(self.file_positions[str(log_file)])
            
            while True:
                line = f.readline()
                
                if line:
                    # Process line
                    try:
                        event = json.loads(line.strip())
                        
                        # Apply filters
                        if event_type and event.get('event_type') != event_type:
                            continue
                        if level and event.get('level') != level:
                            continue
                        
                        # Send event
                        yield self._format_sse("log_event", event)
                        
                        # Update position
                        with self._lock:
                            self.file_positions[str(log_file)] = f.tell()
                        
                    except json.JSONDecodeError:
                        continue
                else:
                    # No more lines
                    if not follow:
                        break
                    
                    # Wait for new content
                    time.sleep(0.1)
                    
                    # Check if file still exists
                    if not log_file.exists():
                        yield self._format_sse("error", {"message": "Log file removed"})
                        break
    
    def _format_sse(self, event_name: str, data: Dict[str, Any]) -> str:
        """
        Format message as Server-Sent Event.
        
        Args:
            event_name: Event name
            data: Event data
            
        Returns:
            SSE formatted string
        """
        return f"event: {event_name}\ndata: {json.dumps(data)}\n\n"
    
    def get_recent_logs(
        self,
        count: int = 50,
        agent_id: Optional[str] = None
    ) -> list:
        """
        Get recent log events (not streaming).
        
        Args:
            count: Number of recent events to return
            agent_id: Filter by agent ID
            
        Returns:
            List of log events
        """
        # Determine which log file to read
        if agent_id:
            log_file = self.logs_dir / f"agent_{agent_id}.jsonl"
        else:
            log_file = self.master_log
        
        if not log_file.exists():
            return []
        
        events = []
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Get last N lines
            for line in lines[-count:]:
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except json.JSONDecodeError:
                    continue
        
        return events
    
    def get_log_summary(self) -> Dict[str, Any]:
        """
        Get summary of session logs.
        
        Returns:
            Summary dictionary
        """
        if not self.master_log.exists():
            return {
                "total_events": 0,
                "agents": [],
                "event_types": {},
                "error_count": 0
            }
        
        summary = {
            "total_events": 0,
            "agents": set(),
            "event_types": {},
            "levels": {},
            "error_count": 0,
            "start_time": None,
            "end_time": None
        }
        
        with open(self.master_log, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    summary["total_events"] += 1
                    
                    # Track agent IDs
                    if event.get('agent_id'):
                        summary["agents"].add(event['agent_id'])
                    
                    # Track event types
                    event_type = event.get('event_type', 'unknown')
                    summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1
                    
                    # Track levels
                    level = event.get('level', 'INFO')
                    summary["levels"][level] = summary["levels"].get(level, 0) + 1
                    
                    # Count errors
                    if level == 'ERROR':
                        summary["error_count"] += 1
                    
                    # Track timestamps
                    timestamp = event.get('timestamp')
                    if timestamp:
                        if summary["start_time"] is None:
                            summary["start_time"] = timestamp
                        summary["end_time"] = timestamp
                    
                except json.JSONDecodeError:
                    continue
        
        summary["agents"] = list(summary["agents"])
        return summary


class ProgressTracker:
    """
    Track workflow progress for real-time updates.
    
    Provides progress information for web UI.
    """
    
    def __init__(self, session_id: str):
        """
        Initialize progress tracker.
        
        Args:
            session_id: Session identifier
        """
        self.session_id = session_id
        self.stages = [
            "Strategic Planning",
            "Market Research",
            "SEO Analysis",
            "Content Creation",
            "Social Media",
            "Quality Validation"
        ]
        self.current_stage = 0
        self.stage_progress = {}
        self.overall_progress = 0.0
        self._lock = threading.Lock()
    
    def update_stage(self, stage_index: int, progress: float = 100.0):
        """
        Update stage progress.
        
        Args:
            stage_index: Index of stage (0-5)
            progress: Progress percentage (0-100)
        """
        with self._lock:
            self.current_stage = stage_index
            self.stage_progress[stage_index] = progress
            self._calculate_overall_progress()
    
    def _calculate_overall_progress(self):
        """Calculate overall workflow progress."""
        if not self.stage_progress:
            self.overall_progress = 0.0
            return
        
        total_stages = len(self.stages)
        completed = sum(
            progress / 100.0 
            for progress in self.stage_progress.values()
        )
        self.overall_progress = (completed / total_stages) * 100.0
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current progress status.
        
        Returns:
            Progress status dictionary
        """
        with self._lock:
            current_stage_name = (
                self.stages[self.current_stage] 
                if self.current_stage < len(self.stages) 
                else "Completed"
            )
            
            return {
                "session_id": self.session_id,
                "current_stage": self.current_stage,
                "current_stage_name": current_stage_name,
                "stage_progress": self.stage_progress,
                "overall_progress": round(self.overall_progress, 2),
                "total_stages": len(self.stages),
                "stages": self.stages
            }


class MetricsCollector:
    """
    Collect and aggregate metrics for real-time display.
    """
    
    def __init__(self, session_id: str):
        """
        Initialize metrics collector.
        
        Args:
            session_id: Session identifier
        """
        self.session_id = session_id
        self.metrics = {
            "agents_executed": 0,
            "tools_called": 0,
            "memory_operations": 0,
            "errors": 0,
            "duration_ms": 0,
            "start_time": None,
            "end_time": None
        }
        self._lock = threading.Lock()
    
    def record_agent_execution(self, agent_id: str, duration_ms: float):
        """Record agent execution."""
        with self._lock:
            self.metrics["agents_executed"] += 1
            self.metrics["duration_ms"] += duration_ms
    
    def record_tool_call(self, tool_name: str):
        """Record tool invocation."""
        with self._lock:
            self.metrics["tools_called"] += 1
    
    def record_memory_operation(self):
        """Record memory operation."""
        with self._lock:
            self.metrics["memory_operations"] += 1
    
    def record_error(self):
        """Record error."""
        with self._lock:
            self.metrics["errors"] += 1
    
    def set_start_time(self):
        """Set workflow start time."""
        with self._lock:
            self.metrics["start_time"] = datetime.now().isoformat()
    
    def set_end_time(self):
        """Set workflow end time."""
        with self._lock:
            self.metrics["end_time"] = datetime.now().isoformat()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        with self._lock:
            return self.metrics.copy()
