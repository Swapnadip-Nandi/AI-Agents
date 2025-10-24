"""
State Tracker for ADK Multi-Agent System
Tracks workflow state, dependencies, and execution progress.
"""

from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class StateTracker:
    """
    Tracks workflow state and manages task dependencies.
    """
    
    def __init__(self, workflow_id: str):
        """
        Initialize state tracker.
        
        Args:
            workflow_id: Unique workflow identifier
        """
        self.workflow_id = workflow_id
        self.workflow_status = TaskStatus.PENDING
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.dependencies: Dict[str, List[str]] = {}
        self.execution_order: List[str] = []
        self.current_stage: Optional[str] = None
        self.checkpoint_data: Dict[str, Any] = {}
        
    def register_task(self, task_id: str, task_name: str, dependencies: Optional[List[str]] = None):
        """
        Register a task in the workflow.
        
        Args:
            task_id: Unique task identifier
            task_name: Human-readable task name
            dependencies: List of task IDs this task depends on
        """
        self.tasks[task_id] = {
            "id": task_id,
            "name": task_name,
            "status": TaskStatus.PENDING,
            "start_time": None,
            "end_time": None,
            "result": None,
            "error": None,
            "retry_count": 0
        }
        
        if dependencies:
            self.dependencies[task_id] = dependencies
        else:
            self.dependencies[task_id] = []
            
    def start_task(self, task_id: str):
        """
        Mark task as started.
        
        Args:
            task_id: Task identifier
        """
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = TaskStatus.RUNNING
            self.tasks[task_id]["start_time"] = datetime.now().isoformat()
            self.execution_order.append(task_id)
            
    def complete_task(self, task_id: str, result: Any):
        """
        Mark task as completed with result.
        
        Args:
            task_id: Task identifier
            result: Task execution result
        """
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = TaskStatus.COMPLETED
            self.tasks[task_id]["end_time"] = datetime.now().isoformat()
            self.tasks[task_id]["result"] = result
            
    def fail_task(self, task_id: str, error: str):
        """
        Mark task as failed.
        
        Args:
            task_id: Task identifier
            error: Error message
        """
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = TaskStatus.FAILED
            self.tasks[task_id]["end_time"] = datetime.now().isoformat()
            self.tasks[task_id]["error"] = error
            
    def retry_task(self, task_id: str):
        """
        Increment retry count for a task.
        
        Args:
            task_id: Task identifier
        """
        if task_id in self.tasks:
            self.tasks[task_id]["retry_count"] += 1
            self.tasks[task_id]["status"] = TaskStatus.PENDING
            
    def can_execute_task(self, task_id: str) -> bool:
        """
        Check if a task can be executed (dependencies met).
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if task can be executed
        """
        if task_id not in self.tasks:
            return False
            
        # Check if all dependencies are completed
        for dep_id in self.dependencies.get(task_id, []):
            if dep_id not in self.tasks:
                return False
            if self.tasks[dep_id]["status"] != TaskStatus.COMPLETED:
                return False
                
        return True
        
    def get_ready_tasks(self) -> List[str]:
        """
        Get list of tasks ready for execution.
        
        Returns:
            List of task IDs
        """
        ready = []
        for task_id, task in self.tasks.items():
            if task["status"] == TaskStatus.PENDING and self.can_execute_task(task_id):
                ready.append(task_id)
        return ready
        
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """
        Get status of a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task status or None
        """
        if task_id in self.tasks:
            return self.tasks[task_id]["status"]
        return None
        
    def get_task_result(self, task_id: str) -> Any:
        """
        Get result of a completed task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task result or None
        """
        if task_id in self.tasks and self.tasks[task_id]["status"] == TaskStatus.COMPLETED:
            return self.tasks[task_id]["result"]
        return None
        
    def get_workflow_progress(self) -> Dict[str, Any]:
        """
        Get overall workflow progress.
        
        Returns:
            Progress statistics
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.FAILED)
        running = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.RUNNING)
        pending = sum(1 for t in self.tasks.values() if t["status"] == TaskStatus.PENDING)
        
        return {
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "running": running,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
            "current_stage": self.current_stage
        }
        
    def set_current_stage(self, stage_id: str, stage_name: str):
        """
        Set the current workflow stage.
        
        Args:
            stage_id: Stage identifier
            stage_name: Stage name
        """
        self.current_stage = {
            "id": stage_id,
            "name": stage_name,
            "started_at": datetime.now().isoformat()
        }
        
    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get detailed execution summary.
        
        Returns:
            Summary dictionary
        """
        return {
            "workflow_id": self.workflow_id,
            "workflow_status": self.workflow_status.value,
            "progress": self.get_workflow_progress(),
            "execution_order": self.execution_order,
            "tasks": {
                task_id: {
                    "name": task["name"],
                    "status": task["status"].value,
                    "duration": self._calculate_duration(task),
                    "retry_count": task["retry_count"]
                }
                for task_id, task in self.tasks.items()
            }
        }
        
    def _calculate_duration(self, task: Dict) -> Optional[float]:
        """Calculate task duration in seconds."""
        if task["start_time"] and task["end_time"]:
            start = datetime.fromisoformat(task["start_time"])
            end = datetime.fromisoformat(task["end_time"])
            return (end - start).total_seconds()
        return None
        
    def create_checkpoint(self) -> Dict[str, Any]:
        """
        Create a state checkpoint.
        
        Returns:
            Checkpoint data
        """
        self.checkpoint_data = {
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "tasks": self.tasks.copy(),
            "execution_order": self.execution_order.copy(),
            "current_stage": self.current_stage
        }
        return self.checkpoint_data
        
    def restore_checkpoint(self, checkpoint_data: Dict[str, Any]):
        """
        Restore state from a checkpoint.
        
        Args:
            checkpoint_data: Checkpoint data to restore
        """
        self.tasks = checkpoint_data["tasks"].copy()
        self.execution_order = checkpoint_data["execution_order"].copy()
        self.current_stage = checkpoint_data["current_stage"]
        
    def export_state(self, file_path: str):
        """
        Export state to JSON file.
        
        Args:
            file_path: Path to save state
        """
        try:
            state_file = Path(file_path)
            state_file.parent.mkdir(parents=True, exist_ok=True)
            
            state = self.get_execution_summary()
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error exporting state: {e}")
            
    def get_failed_tasks(self) -> List[Dict[str, Any]]:
        """
        Get list of failed tasks.
        
        Returns:
            List of failed task details
        """
        return [
            {
                "id": task_id,
                "name": task["name"],
                "error": task["error"],
                "retry_count": task["retry_count"]
            }
            for task_id, task in self.tasks.items()
            if task["status"] == TaskStatus.FAILED
        ]
        
    def has_critical_failure(self) -> bool:
        """
        Check if workflow has critical failures.
        
        Returns:
            True if there are unrecoverable failures
        """
        for task in self.tasks.values():
            if task["status"] == TaskStatus.FAILED and task["retry_count"] >= 3:
                return True
        return False
        
    def get_next_executable_tasks(self, max_parallel: int = 3) -> List[str]:
        """
        Get next tasks that can be executed in parallel.
        
        Args:
            max_parallel: Maximum number of parallel tasks
            
        Returns:
            List of task IDs to execute
        """
        ready_tasks = self.get_ready_tasks()
        return ready_tasks[:max_parallel]
