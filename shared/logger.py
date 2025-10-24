"""
Logger setup for ADK Multi-Agent System
Configurable logging with file and console output using loguru.
"""

import sys
from pathlib import Path
from datetime import datetime
from loguru import logger
import yaml
from typing import Optional


# Global logger configuration
_logger_configured = False


def setup_logger(config_path: str = "./config/logging.yaml") -> None:
    """
    Setup global logger with configuration from YAML.
    
    Args:
        config_path: Path to logging configuration file
    """
    global _logger_configured
    
    if _logger_configured:
        return
    
    # Load logging configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load logging config: {e}. Using defaults.")
        config = _get_default_config()
    
    # Remove default handler
    logger.remove()
    
    log_config = config.get("logging", {})
    
    # Console handler
    if log_config.get("handlers", {}).get("console", {}).get("enabled", True):
        console_level = log_config["handlers"]["console"].get("level", "INFO")
        console_format = _get_format_string(log_config, "console")
        
        logger.add(
            sys.stdout,
            format=console_format,
            level=console_level,
            colorize=log_config["handlers"]["console"].get("colorize", True)
        )
    
    # File handler
    if log_config.get("handlers", {}).get("file", {}).get("enabled", True):
        file_config = log_config["handlers"]["file"]
        log_dir = Path(file_config.get("path", "./storage/logs"))
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"amazon_campaign_{timestamp}.log"
        
        file_level = file_config.get("level", "DEBUG")
        file_format = _get_format_string(log_config, "file")
        
        # File rotation settings
        rotation_config = file_config.get("rotation", {})
        max_size = f"{rotation_config.get('max_size_mb', 10)} MB"
        
        logger.add(
            str(log_file),
            format=file_format,
            level=file_level,
            rotation=max_size,
            retention=rotation_config.get('max_files', 10),
            compression="zip" if rotation_config.get('compress_old', True) else None
        )
    
    # Error file handler
    if log_config.get("handlers", {}).get("error_file", {}).get("enabled", True):
        error_config = log_config["handlers"]["error_file"]
        error_dir = Path(error_config.get("path", "./storage/logs/errors"))
        error_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_file = error_dir / f"errors_{timestamp}.log"
        
        logger.add(
            str(error_file),
            format=_get_format_string(log_config, "error_file"),
            level="ERROR",
            rotation="10 MB",
            retention=10,
            compression="zip"
        )
    
    _logger_configured = True
    logger.info("Logger initialized successfully")


def _get_format_string(config: dict, handler: str) -> str:
    """Get format string for a specific handler."""
    formats = config.get("formats", {})
    handler_config = config.get("handlers", {}).get(handler, {})
    format_type = handler_config.get("format", "detailed")
    
    if format_type == "simple":
        return "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    elif format_type == "json":
        return "{message}"  # JSON formatting would need custom serialization
    else:  # detailed
        return "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"


def _get_default_config() -> dict:
    """Get default logging configuration."""
    return {
        "logging": {
            "enabled": True,
            "handlers": {
                "console": {
                    "enabled": True,
                    "level": "INFO",
                    "format": "detailed",
                    "colorize": True
                },
                "file": {
                    "enabled": True,
                    "level": "DEBUG",
                    "format": "detailed",
                    "path": "./storage/logs",
                    "rotation": {
                        "enabled": True,
                        "max_size_mb": 10,
                        "max_files": 10,
                        "compress_old": True
                    }
                }
            }
        }
    }


def get_logger(name: Optional[str] = None):
    """
    Get configured logger instance.
    
    Args:
        name: Optional name for the logger context
        
    Returns:
        Configured logger instance
    """
    if not _logger_configured:
        setup_logger()
    
    if name:
        return logger.bind(name=name)
    return logger


# Convenience logging functions
def log_agent_start(agent_name: str, agent_id: str):
    """Log agent execution start."""
    logger.info(f"🤖 Agent Started: {agent_name} (ID: {agent_id})")


def log_agent_complete(agent_name: str, agent_id: str, duration: float):
    """Log agent execution completion."""
    logger.success(f"✅ Agent Completed: {agent_name} (ID: {agent_id}) in {duration:.2f}s")


def log_agent_error(agent_name: str, agent_id: str, error: Exception):
    """Log agent execution error."""
    logger.error(f"❌ Agent Error: {agent_name} (ID: {agent_id}) - {str(error)}")


def log_workflow_start(workflow_name: str, workflow_id: str):
    """Log workflow start."""
    logger.info(f"🚀 Workflow Started: {workflow_name} (ID: {workflow_id})")


def log_workflow_complete(workflow_name: str, workflow_id: str, duration: float):
    """Log workflow completion."""
    logger.success(f"🎉 Workflow Completed: {workflow_name} (ID: {workflow_id}) in {duration:.2f}s")


def log_stage_transition(from_stage: str, to_stage: str):
    """Log stage transition."""
    logger.info(f"🔄 Stage Transition: {from_stage} → {to_stage}")


def log_tool_call(tool_name: str, agent_name: str):
    """Log tool invocation."""
    logger.debug(f"🔧 Tool Call: {tool_name} by {agent_name}")


def log_validation_result(passed: bool, score: float, agent_name: str):
    """Log validation result."""
    status = "✅ PASSED" if passed else "❌ FAILED"
    logger.info(f"{status} Validation: {agent_name} scored {score:.1f}/100")


class Logger:
    """
    Logger wrapper class for compatibility with agent imports.
    Provides a simple interface to loguru logger.
    """
    
    def __init__(self, name: str = "ADK"):
        """
        Initialize logger with a name.
        
        Args:
            name: Logger name for context
        """
        self.name = name
        self._logger = get_logger(name)
    
    def info(self, message: str):
        """Log info message."""
        self._logger.info(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self._logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self._logger.error(message)
    
    def success(self, message: str):
        """Log success message."""
        self._logger.success(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self._logger.critical(message)
    
    def exception(self, message: str):
        """Log exception with traceback."""
        self._logger.exception(message)
