"""
Utility functions for LiteAgent.
"""

import os
import json
import logging
import sys
from datetime import datetime

# ANSI color codes for colored terminal output
COLORS = {
    'DEBUG': '\033[36m',     # Cyan
    'INFO': '\033[32m',      # Green
    'WARNING': '\033[33m',   # Yellow
    'ERROR': '\033[31m',     # Red
    'CRITICAL': '\033[41m',  # Red background
    'RESET': '\033[0m',      # Reset to default
    'BOLD': '\033[1m',       # Bold text
    'UNDERLINE': '\033[4m',  # Underlined text
    'TIMESTAMP': '\033[90m', # Gray for timestamp
}

# Level prefixes for better visual distinction
LEVEL_PREFIXES = {
    'DEBUG': '🔍',
    'INFO': '✅',
    'WARNING': '⛔',
    'ERROR': '❌',
    'CRITICAL': '🔥',
}

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages based on level."""
    
    def format(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = f"{color}{COLORS['BOLD']}{prefix} {record.levelname}{COLORS['RESET']}"
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result

# Configure logging
logger = logging.getLogger("liteagent")
logger.setLevel(logging.INFO)

# Console handler with colored output
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s \t| %(message)s'))
logger.addHandler(_console_handler)

def setup_logging(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    _console_handler.setLevel(level)
    
    # Reset handlers if reconfiguring
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    
    # Update console formatter based on color preference
    if use_colors:
        _console_handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s \t| %(message)s'))
    else:
        _console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s \t| %(message)s'))
    
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
    
    # Log examples of each level to demonstrate colors if in debug mode
    if use_colors and level <= logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

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
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
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