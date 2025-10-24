"""
Validation Workflow - Iterative Quality Validation Loop

This workflow implements a validation loop where content is reviewed and can be
sent back for revision if needed.
"""

from typing import Dict, Any, Optional
from shared.logger import Logger


class ValidationWorkflow:
    """
    Validation Workflow - Quality assurance loop
    
    Implements an iterative validation process where content can be
    reviewed, rejected, and revised multiple times until approval.
    """
    
    def __init__(
        self,
        copywriter,
        quality_validator,
        logger: Logger,
        max_iterations: int = 3
    ):
        """
        Initialize validation workflow.
        
        Args:
            copywriter: Copywriter agent
            quality_validator: Quality validator agent
            logger: Logger instance
            max_iterations: Maximum revision iterations
        """
        self.copywriter = copywriter
        self.quality_validator = quality_validator
        self.logger = logger
        self.max_iterations = max_iterations
    
    def execute(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute validation workflow with revision loop.
        
        Args:
            product_info: Product information
            
        Returns:
            Validated content with revision history
        """
        self.logger.info("Starting validation workflow...")
        
        revision_history = []
        iteration = 0
        approved = False
        current_listing = None
        
        while iteration < self.max_iterations and not approved:
            iteration += 1
            self.logger.info(f"\n--- Validation Iteration {iteration}/{self.max_iterations} ---")
            
            # Create or revise content
            if iteration == 1:
                self.logger.info("Creating initial content...")
                current_listing = self.copywriter.create_amazon_listing(product_info)
            else:
                self.logger.info("Revising content based on feedback...")
                current_listing = self._revise_content(
                    current_listing,
                    revision_history[-1]["feedback"]
                )
            
            # Validate content
            self.logger.info("Validating content...")
            validation_result = self.quality_validator.validate_campaign()
            
            approved = validation_result.get("approval", False)
            score = validation_result.get("overall_score", 0)
            
            # Record iteration
            revision_history.append({
                "iteration": iteration,
                "score": score,
                "approved": approved,
                "feedback": validation_result.get("recommendations", []),
                "issues": self._extract_issues(validation_result)
            })
            
            if approved:
                self.logger.success(f"Content approved! Score: {score}/100")
            else:
                self.logger.warning(
                    f"Content needs revision. Score: {score}/100. "
                    f"Issues: {len(revision_history[-1]['issues'])}"
                )
        
        if not approved:
            self.logger.warning(
                f"Content not approved after {self.max_iterations} iterations. "
                "Proceeding with best version."
            )
        
        return {
            "final_listing": current_listing,
            "approved": approved,
            "iterations": iteration,
            "revision_history": revision_history,
            "final_score": revision_history[-1]["score"] if revision_history else 0
        }
    
    def _revise_content(
        self,
        current_listing: Dict[str, Any],
        feedback: list
    ) -> Dict[str, Any]:
        """
        Revise content based on validation feedback.
        
        Args:
            current_listing: Current listing content
            feedback: Validation feedback
            
        Returns:
            Revised listing
        """
        # In a real implementation, this would use the LLM to revise content
        # For now, we simulate revisions by noting the feedback
        
        self.logger.info(f"Applying {len(feedback)} pieces of feedback...")
        
        # Simulate content improvement
        current_listing["revision_notes"] = feedback
        current_listing["revised"] = True
        
        return current_listing
    
    def _extract_issues(self, validation_result: Dict[str, Any]) -> list:
        """Extract all issues from validation result."""
        issues = []
        
        # Extract issues from all validation components
        for key in ["listing_validation", "social_validation", "hallucination_check", "compliance_check"]:
            if key in validation_result:
                component_issues = validation_result[key].get("issues", [])
                if isinstance(component_issues, list):
                    issues.extend(component_issues)
        
        return issues
