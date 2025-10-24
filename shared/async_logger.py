"""
Async Time-Series Logger for ADK Multi-Agent System

Features:
- Non-blocking asynchronous logging
- Session-based log organization
- Time-series event tracking
- Structured JSON logging
- Real-time log streaming support
- Agent-level log isolation

Industry Best Practices:
- Async queue-based logging to prevent blocking
- Structured logging with consistent schema
- Log rotation per session
- Microsecond precision timestamps
- Parent-child relationship tracking for nested operations
"""

import asyncio
import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, asdict, field
from queue import Queue, Empty
from enum import Enum
import time


class LogLevel(Enum):
    """Log severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    METRIC = "METRIC"


class EventType(Enum):
    """Event types for time-series logging."""
    SESSION_STARTED = "session_started"
    SESSION_COMPLETED = "session_completed"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"
    TOOL_CALLED = "tool_called"
    TOOL_COMPLETED = "tool_completed"
    MEMORY_STORED = "memory_stored"
    MEMORY_RETRIEVED = "memory_retrieved"
    WORKFLOW_STAGE = "workflow_stage"
    VALIDATION_RESULT = "validation_result"
    METRIC_RECORDED = "metric_recorded"


@dataclass
class LogEvent:
    """Structured log event."""
    timestamp: str
    session_id: str
    event_type: str
    level: str
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    duration_ms: Optional[float] = None
    parent_event_id: Optional[str] = None
    event_id: str = field(default_factory=lambda: str(int(time.time() * 1000000)))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


class AsyncLogger:
    """
    Asynchronous logger with session-based organization.
    
    Uses a background thread with queue to ensure non-blocking logging.
    All agents share this logger but logs are organized by session and agent.
    """
    
    def __init__(
        self,
        session_id: str,
        session_dir: Path,
        buffer_size: int = 1000,
        flush_interval: float = 1.0
    ):
        """
        Initialize async logger.
        
        Args:
            session_id: Unique session identifier
            session_dir: Session directory for log files
            buffer_size: Size of log buffer
            flush_interval: Seconds between automatic flushes
        """
        self.session_id = session_id
        self.session_dir = Path(session_dir)
        self.logs_dir = self.session_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Log queue for async processing
        self.log_queue: Queue = Queue(maxsize=buffer_size)
        
        # Thread control
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.flush_interval = flush_interval
        
        # Log files
        self.master_log_file = self.logs_dir / "session_timeseries.jsonl"
        self.agent_log_files: Dict[str, Path] = {}
        
        # Performance tracking
        self.events_logged = 0
        self.events_dropped = 0
        
        # Start logging thread
        self.start()
    
    def start(self):
        """Start async logging thread."""
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(
                target=self._log_worker,
                daemon=True,
                name=f"AsyncLogger-{self.session_id[:8]}"
            )
            self.worker_thread.start()
    
    def stop(self):
        """Stop async logging and flush remaining logs."""
        if self.running:
            self.running = False
            self.flush()
            if self.worker_thread:
                self.worker_thread.join(timeout=5.0)
    
    def _log_worker(self):
        """Background worker thread for processing log queue."""
        last_flush = time.time()
        
        while self.running or not self.log_queue.empty():
            try:
                # Get log event with timeout
                try:
                    event = self.log_queue.get(timeout=0.1)
                except Empty:
                    # Check if we need to flush
                    if time.time() - last_flush >= self.flush_interval:
                        self._flush_buffers()
                        last_flush = time.time()
                    continue
                
                # Write event to appropriate files
                self._write_event(event)
                self.events_logged += 1
                self.log_queue.task_done()
                
            except Exception as e:
                print(f"Error in log worker: {e}")
        
        # Final flush
        self._flush_buffers()
    
    def _write_event(self, event: LogEvent):
        """Write event to log files."""
        json_line = event.to_json()
        
        # Write to master session log
        with open(self.master_log_file, 'a', encoding='utf-8') as f:
            f.write(json_line + '\n')
        
        # Write to agent-specific log if applicable
        if event.agent_id:
            agent_log = self._get_agent_log_file(event.agent_id)
            with open(agent_log, 'a', encoding='utf-8') as f:
                f.write(json_line + '\n')
    
    def _get_agent_log_file(self, agent_id: str) -> Path:
        """Get or create agent-specific log file."""
        if agent_id not in self.agent_log_files:
            log_file = self.logs_dir / f"agent_{agent_id}.jsonl"
            self.agent_log_files[agent_id] = log_file
        return self.agent_log_files[agent_id]
    
    def _flush_buffers(self):
        """Flush all file buffers."""
        # File buffers are flushed automatically on close
        pass
    
    def flush(self):
        """Force flush of all pending logs."""
        self.log_queue.join()
        self._flush_buffers()
    
    def log(
        self,
        event_type: EventType,
        level: LogLevel,
        message: str,
        agent_id: Optional[str] = None,
        agent_name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None,
        parent_event_id: Optional[str] = None
    ) -> str:
        """
        Log an event (non-blocking).
        
        Args:
            event_type: Type of event
            level: Log level
            message: Log message
            agent_id: Agent identifier
            agent_name: Agent name
            data: Additional structured data
            duration_ms: Duration in milliseconds
            parent_event_id: Parent event ID for nesting
            
        Returns:
            Event ID for reference
        """
        event = LogEvent(
            timestamp=datetime.now().isoformat(),
            session_id=self.session_id,
            event_type=event_type.value,
            level=level.value,
            agent_id=agent_id,
            agent_name=agent_name,
            message=message,
            data=data or {},
            duration_ms=duration_ms,
            parent_event_id=parent_event_id
        )
        
        try:
            self.log_queue.put_nowait(event)
        except:
            # Queue is full, drop event
            self.events_dropped += 1
        
        return event.event_id
    
    # Convenience methods for different log levels
    
    def debug(self, message: str, agent_id: Optional[str] = None, **kwargs):
        """Log debug message."""
        return self.log(
            EventType.WORKFLOW_STAGE,
            LogLevel.DEBUG,
            message,
            agent_id=agent_id,
            data=kwargs
        )
    
    def info(self, message: str, agent_id: Optional[str] = None, **kwargs):
        """Log info message."""
        return self.log(
            EventType.WORKFLOW_STAGE,
            LogLevel.INFO,
            message,
            agent_id=agent_id,
            data=kwargs
        )
    
    def warning(self, message: str, agent_id: Optional[str] = None, **kwargs):
        """Log warning message."""
        return self.log(
            EventType.WORKFLOW_STAGE,
            LogLevel.WARNING,
            message,
            agent_id=agent_id,
            data=kwargs
        )
    
    def error(self, message: str, agent_id: Optional[str] = None, **kwargs):
        """Log error message."""
        return self.log(
            EventType.AGENT_ERROR,
            LogLevel.ERROR,
            message,
            agent_id=agent_id,
            data=kwargs
        )
    
    def success(self, message: str, agent_id: Optional[str] = None, **kwargs):
        """Log success message."""
        return self.log(
            EventType.WORKFLOW_STAGE,
            LogLevel.SUCCESS,
            message,
            agent_id=agent_id,
            data=kwargs
        )
    
    def agent_started(
        self,
        agent_id: str,
        agent_name: str,
        task: str,
        **kwargs
    ) -> str:
        """Log agent start event."""
        return self.log(
            EventType.AGENT_STARTED,
            LogLevel.INFO,
            f"Agent started: {task}",
            agent_id=agent_id,
            agent_name=agent_name,
            data={"task": task, **kwargs}
        )
    
    def agent_completed(
        self,
        agent_id: str,
        agent_name: str,
        duration_ms: float,
        parent_event_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """Log agent completion event."""
        return self.log(
            EventType.AGENT_COMPLETED,
            LogLevel.SUCCESS,
            f"Agent completed in {duration_ms:.2f}ms",
            agent_id=agent_id,
            agent_name=agent_name,
            duration_ms=duration_ms,
            parent_event_id=parent_event_id,
            data=kwargs
        )
    
    def tool_called(
        self,
        agent_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        **kwargs
    ) -> str:
        """Log tool invocation."""
        return self.log(
            EventType.TOOL_CALLED,
            LogLevel.INFO,
            f"Tool called: {tool_name}",
            agent_id=agent_id,
            data={"tool_name": tool_name, "parameters": parameters, **kwargs}
        )
    
    def memory_operation(
        self,
        agent_id: str,
        operation: str,
        memory_type: str,
        key: str,
        **kwargs
    ) -> str:
        """Log memory operation."""
        event_type = (
            EventType.MEMORY_STORED if operation == "store"
            else EventType.MEMORY_RETRIEVED
        )
        
        return self.log(
            event_type,
            LogLevel.DEBUG,
            f"Memory {operation}: {memory_type}.{key}",
            agent_id=agent_id,
            data={
                "operation": operation,
                "memory_type": memory_type,
                "key": key,
                **kwargs
            }
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get logging statistics."""
        return {
            "session_id": self.session_id,
            "events_logged": self.events_logged,
            "events_dropped": self.events_dropped,
            "queue_size": self.log_queue.qsize(),
            "running": self.running
        }
    
    def read_logs(
        self,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        level: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Read logs with optional filtering.
        
        Args:
            agent_id: Filter by agent ID
            event_type: Filter by event type
            level: Filter by log level
            limit: Maximum number of events to return
            
        Returns:
            List of log events
        """
        # Flush to ensure all logs are written
        self.flush()
        
        # Determine which log file to read
        if agent_id:
            log_file = self._get_agent_log_file(agent_id)
        else:
            log_file = self.master_log_file
        
        if not log_file.exists():
            return []
        
        # Read and filter logs
        events = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    event = json.loads(line.strip())
                    
                    # Apply filters
                    if event_type and event.get('event_type') != event_type:
                        continue
                    if level and event.get('level') != level:
                        continue
                    
                    events.append(event)
                    
                    # Apply limit
                    if limit and len(events) >= limit:
                        break
                        
                except json.JSONDecodeError:
                    continue
        
        return events
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
