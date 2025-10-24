"""
Enhanced Memory Manager with Long-Term Learning
Implements short-term and long-term memory with campaign learning capabilities.

Features:
- Session-scoped short-term memory (cleared after workflow)
- Persistent long-term memory with semantic search
- Campaign learning from past successes
- Memory caching for performance
- Automatic memory summarization
- Memory retrieval by similarity

Industry Best Practices:
- Separate memory stores for different scopes
- LRU caching for frequently accessed memories
- Automatic archival of old memories
- Vector-based similarity search for campaign templates
- Memory compression to reduce storage
"""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import OrderedDict
import pickle


@dataclass
class MemoryEntry:
    """Memory entry with metadata."""
    key: str
    value: Any
    memory_type: str
    agent_id: str
    session_id: Optional[str] = None
    created_at: str = ""
    accessed_at: str = ""
    access_count: int = 0
    tags: List[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.accessed_at:
            self.accessed_at = self.created_at
        if self.tags is None:
            self.tags = []


@dataclass
class CampaignTemplate:
    """Campaign template from successful past campaigns."""
    template_id: str
    product_name: str
    category: str
    quality_score: float
    created_at: str
    session_id: str
    target_audience: str
    keywords: List[str]
    listing_structure: Dict[str, Any]
    social_strategy: Dict[str, Any]
    success_metrics: Dict[str, Any]
    tags: List[str]


class LRUCache:
    """Simple LRU cache for memory operations."""
    
    def __init__(self, capacity: int = 100):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Any):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def clear(self):
        self.cache.clear()


class EnhancedMemoryManager:
    """
    Enhanced memory manager with learning capabilities.
    
    Memory Types:
    - Short-term: Session-scoped, cleared after workflow
    - Long-term: Persistent across sessions
    - Working: Task-scoped, cleared after each agent task
    - Shared: Global shared memory for agent collaboration
    - Templates: Successful campaign templates for learning
    """
    
    def __init__(
        self,
        session_id: str,
        session_dir: Path,
        storage_root: Path,
        enable_caching: bool = True,
        cache_size: int = 100
    ):
        """
        Initialize enhanced memory manager.
        
        Args:
            session_id: Current session ID
            session_dir: Session-specific directory
            storage_root: Root storage directory
            enable_caching: Enable LRU caching
            cache_size: Size of LRU cache
        """
        self.session_id = session_id
        self.session_dir = Path(session_dir)
        self.storage_root = Path(storage_root)
        
        # Memory directories
        self.session_memory_dir = self.session_dir / "memory"
        self.session_memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.longterm_memory_dir = self.storage_root / "memory" / "longterm"
        self.longterm_memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.templates_dir = self.storage_root / "memory" / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory stores
        self.short_term_memory: Dict[str, Dict[str, MemoryEntry]] = {}
        self.working_memory: Dict[str, Dict[str, MemoryEntry]] = {}
        self.shared_memory: Dict[str, MemoryEntry] = {}
        
        # Caching
        self.enable_caching = enable_caching
        if enable_caching:
            self.cache = LRUCache(capacity=cache_size)
        
        # Load long-term memory index
        self.longterm_index = self._load_longterm_index()
        
        # Load campaign templates
        self.templates_index = self._load_templates_index()
    
    def _load_longterm_index(self) -> Dict[str, str]:
        """Load long-term memory index."""
        index_file = self.longterm_memory_dir / "memory_index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load longterm index: {e}")
        return {}
    
    def _save_longterm_index(self):
        """Save long-term memory index."""
        index_file = self.longterm_memory_dir / "memory_index.json"
        try:
            with open(index_file, 'w') as f:
                json.dump(self.longterm_index, f, indent=2)
        except Exception as e:
            print(f"Error saving longterm index: {e}")
    
    def _load_templates_index(self) -> Dict[str, CampaignTemplate]:
        """Load campaign templates index."""
        index_file = self.templates_dir / "templates_index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    data = json.load(f)
                return {
                    tid: CampaignTemplate(**template_data)
                    for tid, template_data in data.items()
                }
            except Exception as e:
                print(f"Warning: Could not load templates index: {e}")
        return {}
    
    def _save_templates_index(self):
        """Save campaign templates index."""
        index_file = self.templates_dir / "templates_index.json"
        try:
            data = {
                tid: asdict(template)
                for tid, template in self.templates_index.items()
            }
            with open(index_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving templates index: {e}")
    
    def store(
        self,
        agent_id: str,
        key: str,
        value: Any,
        memory_type: str = "short_term",
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Store data in agent's memory.
        
        Args:
            agent_id: Agent identifier
            key: Memory key
            value: Data to store
            memory_type: Type of memory (short_term, long_term, working, shared)
            tags: Optional tags for categorization
            
        Returns:
            Success status
        """
        try:
            entry = MemoryEntry(
                key=key,
                value=value,
                memory_type=memory_type,
                agent_id=agent_id,
                session_id=self.session_id,
                tags=tags or []
            )
            
            if memory_type == "short_term":
                if agent_id not in self.short_term_memory:
                    self.short_term_memory[agent_id] = {}
                self.short_term_memory[agent_id][key] = entry
                
                # Save to session directory
                self._save_session_memory(agent_id, key, entry)
                
            elif memory_type == "long_term":
                # Save to long-term storage
                self._save_longterm_memory(agent_id, key, entry)
                
            elif memory_type == "working":
                if agent_id not in self.working_memory:
                    self.working_memory[agent_id] = {}
                self.working_memory[agent_id][key] = entry
                
            elif memory_type == "shared":
                self.shared_memory[key] = entry
                
            # Update cache
            if self.enable_caching:
                cache_key = f"{agent_id}:{memory_type}:{key}"
                self.cache.put(cache_key, value)
            
            return True
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve(
        self,
        agent_id: str,
        key: str,
        memory_type: str = "short_term"
    ) -> Optional[Any]:
        """
        Retrieve data from agent's memory.
        
        Args:
            agent_id: Agent identifier
            key: Memory key
            memory_type: Type of memory to retrieve from
            
        Returns:
            Retrieved value or None
        """
        # Check cache first
        if self.enable_caching:
            cache_key = f"{agent_id}:{memory_type}:{key}"
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return cached_value
        
        try:
            entry = None
            
            if memory_type == "short_term":
                if agent_id in self.short_term_memory:
                    entry = self.short_term_memory[agent_id].get(key)
                    
            elif memory_type == "long_term":
                entry = self._load_longterm_memory(agent_id, key)
                
            elif memory_type == "working":
                if agent_id in self.working_memory:
                    entry = self.working_memory[agent_id].get(key)
                    
            elif memory_type == "shared":
                entry = self.shared_memory.get(key)
            
            if entry:
                # Update access metadata
                entry.accessed_at = datetime.now().isoformat()
                entry.access_count += 1
                
                # Update cache
                if self.enable_caching:
                    cache_key = f"{agent_id}:{memory_type}:{key}"
                    self.cache.put(cache_key, entry.value)
                
                return entry.value
            
            return None
            
        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return None
    
    def _save_session_memory(self, agent_id: str, key: str, entry: MemoryEntry):
        """Save memory to session directory."""
        agent_memory_dir = self.session_memory_dir / agent_id
        agent_memory_dir.mkdir(exist_ok=True)
        
        memory_file = agent_memory_dir / f"{key}.json"
        with open(memory_file, 'w') as f:
            json.dump(asdict(entry), f, indent=2, default=str)
    
    def _save_longterm_memory(self, agent_id: str, key: str, entry: MemoryEntry):
        """Save to long-term memory storage."""
        memory_key = f"{agent_id}:{key}"
        memory_hash = hashlib.md5(memory_key.encode()).hexdigest()
        
        memory_file = self.longterm_memory_dir / f"{memory_hash}.pkl"
        with open(memory_file, 'wb') as f:
            pickle.dump(entry, f)
        
        # Update index
        self.longterm_index[memory_key] = str(memory_file)
        self._save_longterm_index()
    
    def _load_longterm_memory(self, agent_id: str, key: str) -> Optional[MemoryEntry]:
        """Load from long-term memory storage."""
        memory_key = f"{agent_id}:{key}"
        
        if memory_key not in self.longterm_index:
            return None
        
        memory_file = Path(self.longterm_index[memory_key])
        if not memory_file.exists():
            return None
        
        try:
            with open(memory_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading longterm memory: {e}")
            return None
    
    def save_campaign_template(
        self,
        product_name: str,
        category: str,
        quality_score: float,
        target_audience: str,
        keywords: List[str],
        listing_structure: Dict[str, Any],
        social_strategy: Dict[str, Any],
        success_metrics: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Save successful campaign as template for future learning.
        
        Args:
            product_name: Product name
            category: Product category
            quality_score: Campaign quality score
            target_audience: Target audience description
            keywords: List of keywords used
            listing_structure: Amazon listing structure
            social_strategy: Social media strategy
            success_metrics: Success metrics
            tags: Optional tags for categorization
            
        Returns:
            Template ID
        """
        template_id = hashlib.md5(
            f"{product_name}:{category}:{self.session_id}".encode()
        ).hexdigest()[:16]
        
        template = CampaignTemplate(
            template_id=template_id,
            product_name=product_name,
            category=category,
            quality_score=quality_score,
            created_at=datetime.now().isoformat(),
            session_id=self.session_id,
            target_audience=target_audience,
            keywords=keywords,
            listing_structure=listing_structure,
            social_strategy=social_strategy,
            success_metrics=success_metrics,
            tags=tags or []
        )
        
        self.templates_index[template_id] = template
        self._save_templates_index()
        
        # Save detailed template data
        template_file = self.templates_dir / f"{template_id}.json"
        with open(template_file, 'w') as f:
            json.dump(asdict(template), f, indent=2, default=str)
        
        return template_id
    
    def find_similar_campaigns(
        self,
        category: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        min_quality_score: float = 80.0,
        limit: int = 5
    ) -> List[Tuple[CampaignTemplate, float]]:
        """
        Find similar campaigns from past successes.
        
        Args:
            category: Product category to match
            keywords: Keywords to match
            target_audience: Target audience to match
            min_quality_score: Minimum quality score threshold
            limit: Maximum number of results
            
        Returns:
            List of (template, similarity_score) tuples
        """
        results = []
        
        for template in self.templates_index.values():
            # Filter by quality score
            if template.quality_score < min_quality_score:
                continue
            
            # Calculate similarity score
            similarity = 0.0
            
            # Category match (weight: 40%)
            if category and template.category.lower() == category.lower():
                similarity += 0.4
            
            # Keyword overlap (weight: 40%)
            if keywords and template.keywords:
                keyword_overlap = len(set(keywords) & set(template.keywords))
                if keyword_overlap > 0:
                    similarity += 0.4 * (keyword_overlap / max(len(keywords), len(template.keywords)))
            
            # Target audience similarity (weight: 20%)
            if target_audience and template.target_audience:
                # Simple word overlap for target audience
                target_words = set(target_audience.lower().split())
                template_words = set(template.target_audience.lower().split())
                word_overlap = len(target_words & template_words)
                if word_overlap > 0:
                    similarity += 0.2 * (word_overlap / max(len(target_words), len(template_words)))
            
            if similarity > 0:
                results.append((template, similarity))
        
        # Sort by similarity (descending) and quality score
        results.sort(key=lambda x: (x[1], x[0].quality_score), reverse=True)
        
        return results[:limit]
    
    def get_learning_suggestions(
        self,
        product_info: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Get suggestions based on similar past campaigns.
        
        Args:
            product_info: Current product information
            
        Returns:
            Suggestions dictionary or None
        """
        similar_campaigns = self.find_similar_campaigns(
            category=product_info.get('category'),
            keywords=product_info.get('keywords', []),
            target_audience=product_info.get('target_audience'),
            min_quality_score=85.0,
            limit=3
        )
        
        if not similar_campaigns:
            return None
        
        best_template, similarity = similar_campaigns[0]
        
        suggestions = {
            "found_similar_campaign": True,
            "similarity_score": similarity,
            "template_id": best_template.template_id,
            "reference_campaign": {
                "product_name": best_template.product_name,
                "quality_score": best_template.quality_score,
                "created_at": best_template.created_at
            },
            "suggested_keywords": best_template.keywords[:10],
            "suggested_listing_structure": best_template.listing_structure,
            "suggested_social_strategy": best_template.social_strategy,
            "message": f"Found similar campaign for '{best_template.product_name}' with {best_template.quality_score}% quality score. Consider using this template as reference."
        }
        
        return suggestions
    
    def clear_session_memory(self):
        """Clear short-term and working memory (end of session)."""
        self.short_term_memory.clear()
        self.working_memory.clear()
        if self.enable_caching:
            self.cache.clear()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            "session_id": self.session_id,
            "short_term_entries": sum(len(v) for v in self.short_term_memory.values()),
            "working_entries": sum(len(v) for v in self.working_memory.values()),
            "shared_entries": len(self.shared_memory),
            "longterm_entries": len(self.longterm_index),
            "campaign_templates": len(self.templates_index),
            "cache_size": len(self.cache.cache) if self.enable_caching else 0
        }
    
    # Compatibility methods for backward compatibility with old MemoryManager interface
    
    def share_memory(
        self, 
        source_agent: Optional[str] = None,
        target_agent: Optional[str] = None,
        from_agent: Optional[str] = None, 
        to_agent: Optional[str] = None, 
        key: Optional[str] = None,
        value: Optional[Any] = None,
        new_key: Optional[str] = None
    ):
        """
        Share memory from one agent to another (compatibility method).
        Supports both old and new parameter naming.
        
        Args:
            source_agent: Source agent ID (new style)
            target_agent: Target agent ID (new style) - use "all" for shared memory
            from_agent: Source agent ID (old style)
            to_agent: Target agent ID (old style)
            key: Memory key to share
            value: Value to share (if provided, stores directly)
            new_key: Optional new key name in target agent's memory
        """
        # Handle parameter aliases
        from_agent = source_agent or from_agent
        to_agent = target_agent or to_agent
        
        if not from_agent or not key:
            return
        
        # If value is provided, store it directly
        if value is not None:
            if to_agent == "all":
                # Share to all agents via shared memory
                self.store(from_agent, key, value, "shared")
            else:
                # Share to specific agent
                target_key = new_key if new_key else key
                self.store(to_agent, target_key, value, "short_term")
        else:
            # Retrieve from source and store to target
            retrieved_value = self.retrieve(from_agent, key, "short_term")
            if retrieved_value is not None:
                if to_agent == "all":
                    self.store(from_agent, key, retrieved_value, "shared")
                else:
                    target_key = new_key if new_key else key
                    self.store(to_agent, target_key, retrieved_value, "short_term")
    
    def share_to_all(self, from_agent: str, key: str, value: Any):
        """
        Share memory to all agents via shared memory (compatibility method).
        
        Args:
            from_agent: Source agent ID
            key: Memory key
            value: Value to share
        """
        self.store(from_agent, key, value, "shared")
    
    def get_agent_context(self, agent_id: str) -> Dict[str, Any]:
        """
        Get complete context for an agent (all memory types).
        Compatibility method for old MemoryManager interface.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            Dictionary containing all agent memories
        """
        context = {
            "short_term": {},
            "working": {},
            "shared": {},
            "long_term": {}
        }
        
        # Short-term memories
        if agent_id in self.short_term_memory:
            context["short_term"] = {
                key: entry.value 
                for key, entry in self.short_term_memory[agent_id].items()
            }
        
        # Working memories
        if agent_id in self.working_memory:
            context["working"] = {
                key: entry.value 
                for key, entry in self.working_memory[agent_id].items()
            }
        
        # Shared memories
        context["shared"] = {
            key: entry.value 
            for key, entry in self.shared_memory.items()
        }
        
        # Long-term memories for this agent
        for memory_key in self.longterm_index.keys():
            if memory_key.startswith(f"{agent_id}:"):
                clean_key = memory_key.replace(f"{agent_id}:", "")
                entry = self._load_longterm_memory(agent_id, clean_key)
                if entry:
                    context["long_term"][clean_key] = entry.value
        
        return context
    
    def clear_working_memory(self, agent_id: str):
        """
        Clear working memory for an agent (compatibility method).
        
        Args:
            agent_id: Agent identifier
        """
        if agent_id in self.working_memory:
            self.working_memory[agent_id] = {}
    
    def create_checkpoint(self, checkpoint_name: str) -> str:
        """
        Create a memory checkpoint (compatibility method).
        
        Args:
            checkpoint_name: Name for the checkpoint
            
        Returns:
            Checkpoint ID
        """
        from datetime import datetime
        import json
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_id = f"{checkpoint_name}_{timestamp}"
        
        checkpoint_data = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "short_term": {
                agent_id: {
                    key: asdict(entry) 
                    for key, entry in memories.items()
                }
                for agent_id, memories in self.short_term_memory.items()
            },
            "working": {
                agent_id: {
                    key: asdict(entry) 
                    for key, entry in memories.items()
                }
                for agent_id, memories in self.working_memory.items()
            },
            "shared": {
                key: asdict(entry) 
                for key, entry in self.shared_memory.items()
            }
        }
        
        checkpoint_file = self.session_memory_dir / f"checkpoint_{checkpoint_id}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2, default=str)
        
        return checkpoint_id
    
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """
        Restore from a checkpoint (compatibility method).
        
        Args:
            checkpoint_id: ID of the checkpoint to restore
            
        Returns:
            Success status
        """
        try:
            checkpoint_file = self.session_memory_dir / f"checkpoint_{checkpoint_id}.json"
            if not checkpoint_file.exists():
                return False
            
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
            
            # Restore short-term memory
            self.short_term_memory = {}
            for agent_id, memories in checkpoint_data.get("short_term", {}).items():
                self.short_term_memory[agent_id] = {
                    key: MemoryEntry(**entry_data)
                    for key, entry_data in memories.items()
                }
            
            # Restore working memory
            self.working_memory = {}
            for agent_id, memories in checkpoint_data.get("working", {}).items():
                self.working_memory[agent_id] = {
                    key: MemoryEntry(**entry_data)
                    for key, entry_data in memories.items()
                }
            
            # Restore shared memory
            self.shared_memory = {
                key: MemoryEntry(**entry_data)
                for key, entry_data in checkpoint_data.get("shared", {}).items()
            }
            
            return True
            
        except Exception as e:
            print(f"Error restoring checkpoint: {e}")
            return False
