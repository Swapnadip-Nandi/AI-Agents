"""
Context Manager for ADK Multi-Agent System
Manages context propagation and data flow between agents.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json


class ContextManager:
    """
    Manages context and data flow between agents in the workflow.
    Handles context propagation rules and data transformation.
    """
    
    def __init__(self, workflow_config: Dict):
        """
        Initialize context manager.
        
        Args:
            workflow_config: Workflow configuration dictionary
        """
        self.workflow_config = workflow_config
        self.workflow_context: Dict[str, Any] = {}
        self.agent_outputs: Dict[str, Any] = {}
        self.propagation_rules = self._load_propagation_rules()
        
    def _load_propagation_rules(self) -> Dict:
        """Load context propagation rules from workflow config."""
        if "data_flow" in self.workflow_config:
            return self.workflow_config["data_flow"].get("context_propagation", [])
        return []
    
    def initialize_workflow_context(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initialize workflow context with input data.
        
        Args:
            initial_data: Initial input data for the workflow
            
        Returns:
            Initialized context dictionary
        """
        self.workflow_context = {
            "workflow_id": self._generate_workflow_id(),
            "started_at": datetime.now().isoformat(),
            "input_data": initial_data,
            "product_info": initial_data.get("product_info", {}),
            "campaign_params": initial_data.get("campaign_params", {}),
            "current_stage": None,
            "completed_stages": [],
            "agent_outputs": {}
        }
        return self.workflow_context
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        return f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def update_stage(self, stage_id: str, stage_name: str):
        """
        Update current workflow stage.
        
        Args:
            stage_id: Stage identifier
            stage_name: Human-readable stage name
        """
        self.workflow_context["current_stage"] = {
            "id": stage_id,
            "name": stage_name,
            "started_at": datetime.now().isoformat()
        }
    
    def complete_stage(self, stage_id: str):
        """
        Mark stage as completed.
        
        Args:
            stage_id: Stage identifier
        """
        if self.workflow_context["current_stage"]["id"] == stage_id:
            completed_stage = self.workflow_context["current_stage"].copy()
            completed_stage["completed_at"] = datetime.now().isoformat()
            self.workflow_context["completed_stages"].append(completed_stage)
            self.workflow_context["current_stage"] = None
    
    def store_agent_output(self, agent_id: str, agent_name: str, output: Any):
        """
        Store output from an agent.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent name
            output: Agent's output data
        """
        self.agent_outputs[agent_id] = {
            "agent_name": agent_name,
            "output": output,
            "timestamp": datetime.now().isoformat()
        }
        self.workflow_context["agent_outputs"][agent_id] = output
    
    def get_agent_output(self, agent_id: str) -> Optional[Any]:
        """
        Retrieve output from a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Agent output or None
        """
        if agent_id in self.agent_outputs:
            return self.agent_outputs[agent_id]["output"]
        return None
    
    def build_agent_context(self, agent_id: str, agent_name: str) -> Dict[str, Any]:
        """
        Build context for a specific agent based on propagation rules.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent name
            
        Returns:
            Context dictionary for the agent
        """
        context = {
            "workflow_id": self.workflow_context["workflow_id"],
            "agent_id": agent_id,
            "agent_name": agent_name,
            "product_info": self.workflow_context["product_info"],
            "campaign_params": self.workflow_context["campaign_params"],
            "current_stage": self.workflow_context["current_stage"]
        }
        
        # Apply propagation rules
        for rule in self.propagation_rules:
            if agent_id in rule.get("to", []) or agent_name.lower().replace(" ", "_") in rule.get("to", []):
                from_agent = rule.get("from")
                fields = rule.get("fields", [])
                
                # Get output from the source agent
                from_output = self.get_agent_output(from_agent)
                if from_output:
                    for field in fields:
                        if isinstance(from_output, dict) and field in from_output:
                            context[field] = from_output[field]
        
        # Add all previous agent outputs for reference
        context["previous_outputs"] = self.agent_outputs.copy()
        
        return context
    
    def propagate_context(self, from_agent: str, to_agents: List[str], fields: List[str]):
        """
        Manually propagate specific fields from one agent to others.
        
        Args:
            from_agent: Source agent ID
            to_agents: List of target agent IDs
            fields: List of field names to propagate
        """
        from_output = self.get_agent_output(from_agent)
        if not from_output:
            return
        
        for to_agent in to_agents:
            if to_agent not in self.agent_outputs:
                self.agent_outputs[to_agent] = {
                    "agent_name": to_agent,
                    "output": {},
                    "timestamp": datetime.now().isoformat()
                }
            
            for field in fields:
                if isinstance(from_output, dict) and field in from_output:
                    if not isinstance(self.agent_outputs[to_agent]["output"], dict):
                        self.agent_outputs[to_agent]["output"] = {}
                    self.agent_outputs[to_agent]["output"][field] = from_output[field]
    
    def get_full_context(self) -> Dict[str, Any]:
        """
        Get complete workflow context.
        
        Returns:
            Full context dictionary
        """
        return self.workflow_context.copy()
    
    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get summarized context (for logging/monitoring).
        
        Returns:
            Summarized context
        """
        return {
            "workflow_id": self.workflow_context["workflow_id"],
            "started_at": self.workflow_context["started_at"],
            "current_stage": self.workflow_context["current_stage"],
            "completed_stages_count": len(self.workflow_context["completed_stages"]),
            "agents_completed": len(self.agent_outputs),
            "product_name": self.workflow_context["product_info"].get("product_name", "N/A")
        }
    
    def export_context(self, file_path: str):
        """
        Export context to JSON file.
        
        Args:
            file_path: Path to save context
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.workflow_context, f, indent=2)
        except Exception as e:
            print(f"Error exporting context: {e}")
    
    def merge_parallel_outputs(self, agent_ids: List[str]) -> Dict[str, Any]:
        """
        Merge outputs from parallel agents.
        
        Args:
            agent_ids: List of agent IDs that ran in parallel
            
        Returns:
            Merged output dictionary
        """
        merged = {}
        for agent_id in agent_ids:
            output = self.get_agent_output(agent_id)
            if output:
                if isinstance(output, dict):
                    merged.update(output)
                else:
                    merged[agent_id] = output
        return merged
    
    def clear_context(self):
        """Clear all context (for cleanup or reset)."""
        self.workflow_context = {}
        self.agent_outputs = {}
