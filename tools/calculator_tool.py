"""
Calculator Tool (Simple Custom Tool)
Provides basic mathematical calculations for agents.
"""

from typing import Any, Dict, List, Optional
import re
import math


class CalculatorTool:
    """
    Simple calculator tool for mathematical operations.
    Useful for ROI calculations, pricing, metrics, etc.
    """
    
    def __init__(self):
        """Initialize calculator."""
        self.calculation_history: List[Dict] = []
        
    def calculate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            Calculation result
        """
        try:
            # Sanitize input - only allow numbers, operators, and parentheses
            safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Evaluate safely
            result = eval(safe_expr, {"__builtins__": {}}, {})
            
            # Log calculation
            self.calculation_history.append({
                "expression": expression,
                "result": result
            })
            
            return float(result)
            
        except Exception as e:
            print(f"Calculation error: {e}")
            return 0.0
            
    def percentage(self, value: float, percentage: float) -> float:
        """
        Calculate percentage of a value.
        
        Args:
            value: Base value
            percentage: Percentage (e.g., 20 for 20%)
            
        Returns:
            Percentage amount
        """
        return (value * percentage) / 100
        
    def percentage_increase(self, old_value: float, new_value: float) -> float:
        """
        Calculate percentage increase.
        
        Args:
            old_value: Original value
            new_value: New value
            
        Returns:
            Percentage increase
        """
        if old_value == 0:
            return 0.0
        return ((new_value - old_value) / old_value) * 100
        
    def roi(self, profit: float, investment: float) -> float:
        """
        Calculate Return on Investment.
        
        Args:
            profit: Profit amount
            investment: Investment amount
            
        Returns:
            ROI percentage
        """
        if investment == 0:
            return 0.0
        return (profit / investment) * 100
        
    def average(self, values: List[float]) -> float:
        """
        Calculate average of values.
        
        Args:
            values: List of numbers
            
        Returns:
            Average value
        """
        if not values:
            return 0.0
        return sum(values) / len(values)
        
    def margin(self, cost: float, price: float) -> float:
        """
        Calculate profit margin.
        
        Args:
            cost: Cost price
            price: Selling price
            
        Returns:
            Profit margin percentage
        """
        if price == 0:
            return 0.0
        return ((price - cost) / price) * 100
        
    def compound_growth(self, initial: float, rate: float, periods: int) -> float:
        """
        Calculate compound growth.
        
        Args:
            initial: Initial value
            rate: Growth rate (as decimal, e.g., 0.05 for 5%)
            periods: Number of periods
            
        Returns:
            Final value after compound growth
        """
        return initial * math.pow((1 + rate), periods)
        
    def break_even(self, fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> float:
        """
        Calculate break-even point in units.
        
        Args:
            fixed_costs: Total fixed costs
            price_per_unit: Selling price per unit
            variable_cost_per_unit: Variable cost per unit
            
        Returns:
            Break-even units
        """
        contribution_margin = price_per_unit - variable_cost_per_unit
        if contribution_margin == 0:
            return 0.0
        return fixed_costs / contribution_margin
        
    def keyword_density(self, keyword: str, total_words: int, keyword_count: int) -> float:
        """
        Calculate keyword density.
        
        Args:
            keyword: Keyword phrase
            total_words: Total word count
            keyword_count: Number of times keyword appears
            
        Returns:
            Keyword density percentage
        """
        if total_words == 0:
            return 0.0
        return (keyword_count / total_words) * 100
        
    def conversion_rate(self, conversions: int, visitors: int) -> float:
        """
        Calculate conversion rate.
        
        Args:
            conversions: Number of conversions
            visitors: Total number of visitors
            
        Returns:
            Conversion rate percentage
        """
        if visitors == 0:
            return 0.0
        return (conversions / visitors) * 100
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to ADK-compatible dictionary format."""
        return {
            "name": "calculator",
            "description": "Perform mathematical calculations including percentages, ROI, margins, and business metrics.",
            "parameters": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate or operation name"
                },
                "values": {
                    "type": "object",
                    "description": "Values for specific calculations (optional)",
                    "optional": True
                }
            }
        }
