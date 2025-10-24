"""
Memory Manager for ADK Multi-Agent System
Handles memory persistence, retrieval, and context management across agents.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
import hashlib


class MemoryManager:
    """
    Enterprise-grade memory manager with file-based persistence.
    Supports short-term, long-term, working, and shared memory types.
    """
    
    def __init__(self, config_path: str = "./config/memory_config.yaml"):
        """Initialize memory manager with configuration."""
        self.config = self._load_config(config_path)
        self.storage_path = Path(self.config["memory"]["file_backend"]["storage_path"])
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory stores
        self.short_term_memory: Dict[str, Dict] = {}
        self.long_term_memory: Dict[str, Any] = {}
        self.working_memory: Dict[str, Dict] = {}
        self.shared_memory: Dict[str, Any] = {}
        
        # Load persisted memory
        self._load_persisted_memory()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load memory configuration from YAML."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_persisted_memory(self):
        """Load long-term memory from disk."""
        long_term_file = self.storage_path / "long_term_memory.json"
        if long_term_file.exists():
            try:
                with open(long_term_file, 'r') as f:
                    self.long_term_memory = json.load(f)
                self._cleanup_old_memories()
            except Exception as e:
                print(f"Error loading persisted memory: {e}")
    
    def _cleanup_old_memories(self):
        """Remove memories older than retention period."""
        retention_days = self.config["memory"]["types"]["long_term"]["retention_days"]
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        keys_to_remove = []
        for key, value in self.long_term_memory.items():
            if isinstance(value, dict) and "timestamp" in value:
                memory_date = datetime.fromisoformat(value["timestamp"])
                if memory_date < cutoff_date:
                    keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.long_term_memory[key]
    
    def store(self, agent_id: str, key: str, value: Any, memory_type: str = "short_term") -> bool:
        """
        Store data in agent's memory.
        
        Args:
            agent_id: Unique identifier for the agent
            key: Memory key
            value: Data to store
            memory_type: Type of memory (short_term, long_term, working, shared)
            
        Returns:
            Success status
        """
        try:
            timestamp = datetime.now().isoformat()
            memory_entry = {
                "value": value,
                "timestamp": timestamp,
                "agent_id": agent_id,
                "type": memory_type
            }
            
            if memory_type == "short_term":
                if agent_id not in self.short_term_memory:
                    self.short_term_memory[agent_id] = {}
                self.short_term_memory[agent_id][key] = memory_entry
                
            elif memory_type == "long_term":
                memory_key = f"{agent_id}:{key}"
                self.long_term_memory[memory_key] = memory_entry
                self._persist_long_term_memory()
                
            elif memory_type == "working":
                if agent_id not in self.working_memory:
                    self.working_memory[agent_id] = {}
                self.working_memory[agent_id][key] = memory_entry
                
            elif memory_type == "shared":
                self.shared_memory[key] = memory_entry
                
            return True
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve(self, agent_id: str, key: str, memory_type: str = "short_term") -> Optional[Any]:
        """
        Retrieve data from agent's memory.
        
        Args:
            agent_id: Unique identifier for the agent
            key: Memory key
            memory_type: Type of memory to retrieve from
            
        Returns:
            Retrieved value or None
        """
        try:
            if memory_type == "short_term":
                if agent_id in self.short_term_memory and key in self.short_term_memory[agent_id]:
                    return self.short_term_memory[agent_id][key]["value"]
                    
            elif memory_type == "long_term":
                memory_key = f"{agent_id}:{key}"
                if memory_key in self.long_term_memory:
                    return self.long_term_memory[memory_key]["value"]
                    
            elif memory_type == "working":
                if agent_id in self.working_memory and key in self.working_memory[agent_id]:
                    return self.working_memory[agent_id][key]["value"]
                    
            elif memory_type == "shared":
                if key in self.shared_memory:
                    return self.shared_memory[key]["value"]
                    
            return None
            
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return None
    
    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """
        Get complete context for an agent (all memory types).
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            Dictionary containing all agent memories
        """
        context = {
            "short_term": self.short_term_memory.get(agent_id, {}),
            "working": self.working_memory.get(agent_id, {}),
            "shared": self.shared_memory.copy(),
            "long_term": {}
        }
        
        # Add relevant long-term memories
        for key, value in self.long_term_memory.items():
            if key.startswith(f"{agent_id}:"):
                clean_key = key.replace(f"{agent_id}:", "")
                context["long_term"][clean_key] = value
        
        return context
    
    def share_memory(self, from_agent: str, to_agent: str, key: str, new_key: Optional[str] = None):
        """
        Share memory from one agent to another.
        
        Args:
            from_agent: Source agent ID
            to_agent: Target agent ID
            key: Memory key to share
            new_key: Optional new key name in target agent's memory
        """
        value = self.retrieve(from_agent, key, "short_term")
        if value is not None:
            target_key = new_key if new_key else key
            self.store(to_agent, target_key, value, "short_term")
    
    def share_to_all(self, from_agent: str, key: str, value: Any):
        """
        Share memory to all agents via shared memory.
        
        Args:
            from_agent: Source agent ID
            key: Memory key
            value: Value to share
        """
        self.store(from_agent, key, value, "shared")
    
    def clear_working_memory(self, agent_id: str):
        """Clear working memory for an agent."""
        if agent_id in self.working_memory:
            self.working_memory[agent_id] = {}
    
    def clear_session_memory(self):
        """Clear all short-term and working memory (end of session)."""
        self.short_term_memory = {}
        self.working_memory = {}
    
    def _persist_long_term_memory(self):
        """Persist long-term memory to disk."""
        try:
            long_term_file = self.storage_path / "long_term_memory.json"
            with open(long_term_file, 'w') as f:
                json.dump(self.long_term_memory, f, indent=2)
        except Exception as e:
            print(f"Error persisting memory: {e}")
    
    def create_checkpoint(self, checkpoint_name: str) -> str:
        """
        Create a memory checkpoint.
        
        Args:
            checkpoint_name: Name for the checkpoint
            
        Returns:
            Checkpoint ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_id = f"{checkpoint_name}_{timestamp}"
        
        checkpoint_data = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "short_term": self.short_term_memory.copy(),
            "working": self.working_memory.copy(),
            "shared": self.shared_memory.copy()
        }
        
        checkpoint_file = self.storage_path / f"checkpoint_{checkpoint_id}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        
        return checkpoint_id
    
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Restore from a checkpoint.
        
        Args:
            checkpoint_id: ID of the checkpoint to restore
            
        Returns:
            Success status
        """
        try:
            checkpoint_file = self.storage_path / f"checkpoint_{checkpoint_id}.json"
            if not checkpoint_file.exists():
                return False
            
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            self.short_term_memory = checkpoint_data["short_term"]
            self.working_memory = checkpoint_data["working"]
            self.shared_memory = checkpoint_data["shared"]
            
            return True
            
        except Exception as e:
            print(f"Error restoring checkpoint: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            "short_term_entries": sum(len(v) for v in self.short_term_memory.values()),
            "long_term_entries": len(self.long_term_memory),
            "working_entries": sum(len(v) for v in self.working_memory.values()),
            "shared_entries": len(self.shared_memory),
            "total_agents": len(set(list(self.short_term_memory.keys()) + 
                                   list(self.working_memory.keys())))
        }
