"""
Utility functions for LiteAgent.
"""

import os
import json
import logging
import sys
from datetime import datetime

# Configure logging
logger = logging.getLogger("liteagent")
logger.setLevel(logging.INFO)

# Console handler
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logger.addHandler(_console_handler)

def setup_logging(log_level="INFO", log_to_file=False, log_file=None):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
    """
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    _console_handler.setLevel(level)
    
    # Reset handlers if reconfiguring
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    
    # Add file handler if requested
    if log_to_file:
        if log_file is None:
            log_file = f"liteagent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        ))
        logger.addHandler(file_handler)
        
    logger.debug(f"Logging initialized at level {log_level}")

def log_completion_request(model, messages, functions=None, **kwargs):
    """Log a completion request in a structured format."""
    logger.debug(
        f"Request: model={model}, messages={len(messages)} messages, "
        f"functions={len(functions) if functions else 0}"
    )

def log_completion_response(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def check_api_keys():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        logger.info(f"{status} {key} found")
        
    return keys

def safe_json_serialize(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(obj, indent=2)
    except (TypeError, ValueError):
        return str(obj)