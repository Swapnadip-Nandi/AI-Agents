"""
Session Manager for ADK Multi-Agent System
Manages session lifecycle, unique session IDs, and session-based operations.

Features:
- Unique session ID generation
- Session-scoped logging
- Session metadata tracking
- Session cleanup and archival
- Session replay capabilities
"""

import uuid
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import threading


@dataclass
class SessionMetadata:
    """Session metadata structure."""
    session_id: str
    created_at: str
    status: str  # 'running', 'completed', 'failed', 'archived'
    product_name: Optional[str] = None
    workflow_type: str = "amazon_campaign"
    duration_seconds: float = 0.0
    agent_count: int = 0
    error_count: int = 0
    quality_score: Optional[float] = None
    completed_at: Optional[str] = None
    archived_at: Optional[str] = None


class SessionManager:
    """
    Manages workflow sessions with unique IDs and lifecycle tracking.
    
    Industry Best Practices:
    - UUID-based session IDs for uniqueness
    - Thread-safe session operations
    - Automatic session cleanup after 7 days
    - Session metadata indexing for quick retrieval
    - Session isolation (logs, memory, results per session)
    """
    
    def __init__(
        self,
        storage_root: str = "./storage",
        retention_days: int = 7,
        auto_cleanup: bool = True
    ):
        """
        Initialize session manager.
        
        Args:
            storage_root: Root directory for storage
            retention_days: Days to retain completed sessions
            auto_cleanup: Enable automatic cleanup of old sessions
        """
        self.storage_root = Path(storage_root)
        self.sessions_root = self.storage_root / "sessions"
        self.sessions_root.mkdir(parents=True, exist_ok=True)
        
        self.retention_days = retention_days
        self.auto_cleanup = auto_cleanup
        
        # Session index file
        self.index_file = self.storage_root / "session_index.json"
        self.sessions_index: Dict[str, SessionMetadata] = self._load_index()
        
        # Thread lock for concurrent access
        self._lock = threading.Lock()
        
        # Run cleanup on initialization if enabled
        if self.auto_cleanup:
            self.cleanup_old_sessions()
    
    def _load_index(self) -> Dict[str, SessionMetadata]:
        """Load session index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                return {
                    sid: SessionMetadata(**meta)
                    for sid, meta in data.items()
                }
            except Exception as e:
                print(f"Warning: Could not load session index: {e}")
        return {}
    
    def _save_index(self):
        """Save session index to disk."""
        try:
            data = {
                sid: asdict(meta)
                for sid, meta in self.sessions_index.items()
            }
            with open(self.index_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving session index: {e}")
    
    def create_session(
        self,
        product_name: Optional[str] = None,
        workflow_type: str = "amazon_campaign"
    ) -> str:
        """
        Create a new session with unique ID.
        
        Args:
            product_name: Name of product for this session
            workflow_type: Type of workflow being executed
            
        Returns:
            Unique session ID (UUID)
        """
        with self._lock:
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create session directory structure
            session_dir = self.sessions_root / session_id
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            (session_dir / "logs").mkdir(exist_ok=True)
            (session_dir / "memory").mkdir(exist_ok=True)
            (session_dir / "results").mkdir(exist_ok=True)
            (session_dir / "agent_outputs").mkdir(exist_ok=True)
            
            # Create session metadata
            metadata = SessionMetadata(
                session_id=session_id,
                created_at=datetime.now().isoformat(),
                status="running",
                product_name=product_name,
                workflow_type=workflow_type
            )
            
            # Save metadata
            self.sessions_index[session_id] = metadata
            self._save_session_metadata(session_id, metadata)
            self._save_index()
            
            return session_id
    
    def _save_session_metadata(self, session_id: str, metadata: SessionMetadata):
        """Save session metadata to session directory."""
        session_dir = self.sessions_root / session_id
        metadata_file = session_dir / "session_manifest.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)
    
    def update_session(
        self,
        session_id: str,
        status: Optional[str] = None,
        duration: Optional[float] = None,
        agent_count: Optional[int] = None,
        error_count: Optional[int] = None,
        quality_score: Optional[float] = None
    ):
        """
        Update session metadata.
        
        Args:
            session_id: Session ID to update
            status: New status
            duration: Execution duration
            agent_count: Number of agents executed
            error_count: Number of errors encountered
            quality_score: Final quality score
        """
        with self._lock:
            if session_id not in self.sessions_index:
                return
            
            metadata = self.sessions_index[session_id]
            
            if status:
                metadata.status = status
                if status in ['completed', 'failed']:
                    metadata.completed_at = datetime.now().isoformat()
            
            if duration is not None:
                metadata.duration_seconds = duration
            
            if agent_count is not None:
                metadata.agent_count = agent_count
            
            if error_count is not None:
                metadata.error_count = error_count
            
            if quality_score is not None:
                metadata.quality_score = quality_score
            
            self._save_session_metadata(session_id, metadata)
            self._save_index()
    
    def get_session_dir(self, session_id: str) -> Path:
        """Get session directory path."""
        return self.sessions_root / session_id
    
    def get_session_metadata(self, session_id: str) -> Optional[SessionMetadata]:
        """Get session metadata."""
        return self.sessions_index.get(session_id)
    
    def list_sessions(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[SessionMetadata]:
        """
        List sessions with optional filtering.
        
        Args:
            status: Filter by status
            limit: Maximum number of sessions to return
            
        Returns:
            List of session metadata
        """
        sessions = list(self.sessions_index.values())
        
        # Filter by status
        if status:
            sessions = [s for s in sessions if s.status == status]
        
        # Sort by creation time (newest first)
        sessions.sort(key=lambda s: s.created_at, reverse=True)
        
        # Apply limit
        if limit:
            sessions = sessions[:limit]
        
        return sessions
    
    def cleanup_old_sessions(self) -> int:
        """
        Clean up sessions older than retention period.
        
        Returns:
            Number of sessions cleaned up
        """
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        cleanup_count = 0
        
        with self._lock:
            sessions_to_cleanup = []
            
            for session_id, metadata in self.sessions_index.items():
                # Parse creation date
                created_at = datetime.fromisoformat(metadata.created_at)
                
                # Check if session is old enough and completed/failed
                if created_at < cutoff_date and metadata.status in ['completed', 'failed']:
                    sessions_to_cleanup.append(session_id)
            
            # Archive and delete old sessions
            for session_id in sessions_to_cleanup:
                if self._archive_session(session_id):
                    cleanup_count += 1
            
            self._save_index()
        
        return cleanup_count
    
    def _archive_session(self, session_id: str) -> bool:
        """
        Archive a session (compress and move to archive).
        
        Args:
            session_id: Session ID to archive
            
        Returns:
            Success status
        """
        try:
            session_dir = self.sessions_root / session_id
            
            if not session_dir.exists():
                return False
            
            # Create archive directory
            archive_dir = self.storage_root / "archive"
            archive_dir.mkdir(exist_ok=True)
            
            # Create compressed archive
            archive_path = archive_dir / f"{session_id}"
            shutil.make_archive(str(archive_path), 'zip', session_dir)
            
            # Remove original session directory
            shutil.rmtree(session_dir)
            
            # Update metadata
            if session_id in self.sessions_index:
                self.sessions_index[session_id].status = "archived"
                self.sessions_index[session_id].archived_at = datetime.now().isoformat()
            
            return True
            
        except Exception as e:
            print(f"Error archiving session {session_id}: {e}")
            return False
    
    def cleanup_session(self, session_id: str) -> bool:
        """
        Manually cleanup a specific session.
        
        Args:
            session_id: Session ID to cleanup
            
        Returns:
            Success status
        """
        with self._lock:
            return self._archive_session(session_id)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about all sessions."""
        stats = {
            "total_sessions": len(self.sessions_index),
            "running": 0,
            "completed": 0,
            "failed": 0,
            "archived": 0,
            "avg_duration": 0.0,
            "avg_quality_score": 0.0,
            "total_errors": 0
        }
        
        durations = []
        quality_scores = []
        
        for metadata in self.sessions_index.values():
            stats[metadata.status] = stats.get(metadata.status, 0) + 1
            stats["total_errors"] += metadata.error_count
            
            if metadata.duration_seconds > 0:
                durations.append(metadata.duration_seconds)
            
            if metadata.quality_score is not None:
                quality_scores.append(metadata.quality_score)
        
        if durations:
            stats["avg_duration"] = sum(durations) / len(durations)
        
        if quality_scores:
            stats["avg_quality_score"] = sum(quality_scores) / len(quality_scores)
        
        return stats
