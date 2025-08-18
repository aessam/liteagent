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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages based on level."""
    
    def xǁColoredFormatterǁformat__mutmut_orig(self, record):
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
    
    def xǁColoredFormatterǁformat__mutmut_1(self, record):
        # Save original values to restore them later
        orig_levelname = None
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
    
    def xǁColoredFormatterǁformat__mutmut_2(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = None
        
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
    
    def xǁColoredFormatterǁformat__mutmut_3(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = None
        
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
    
    def xǁColoredFormatterǁformat__mutmut_4(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['XXTIMESTAMPXX']}{self.formatTime(record)}{COLORS['RESET']}"
        
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
    
    def xǁColoredFormatterǁformat__mutmut_5(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['timestamp']}{self.formatTime(record)}{COLORS['RESET']}"
        
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
    
    def xǁColoredFormatterǁformat__mutmut_6(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(None)}{COLORS['RESET']}"
        
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
    
    def xǁColoredFormatterǁformat__mutmut_7(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['XXRESETXX']}"
        
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
    
    def xǁColoredFormatterǁformat__mutmut_8(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['reset']}"
        
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
    
    def xǁColoredFormatterǁformat__mutmut_9(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname not in COLORS:
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
    
    def xǁColoredFormatterǁformat__mutmut_10(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = None
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
    
    def xǁColoredFormatterǁformat__mutmut_11(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = None
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
    
    def xǁColoredFormatterǁformat__mutmut_12(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(None, '')
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
    
    def xǁColoredFormatterǁformat__mutmut_13(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, None)
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
    
    def xǁColoredFormatterǁformat__mutmut_14(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get('')
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
    
    def xǁColoredFormatterǁformat__mutmut_15(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, )
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
    
    def xǁColoredFormatterǁformat__mutmut_16(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, 'XXXX')
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
    
    def xǁColoredFormatterǁformat__mutmut_17(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = None
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_18(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = f"{color}{COLORS['XXBOLDXX']}{prefix} {record.levelname}{COLORS['RESET']}"
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_19(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = f"{color}{COLORS['bold']}{prefix} {record.levelname}{COLORS['RESET']}"
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_20(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = f"{color}{COLORS['BOLD']}{prefix} {record.levelname}{COLORS['XXRESETXX']}"
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_21(self, record):
        # Save original values to restore them later
        orig_levelname = record.levelname
        orig_msg = record.msg
        
        # Format timestamp with gray color
        record.asctime = f"{COLORS['TIMESTAMP']}{self.formatTime(record)}{COLORS['RESET']}"
        
        # Format level name with appropriate color, make it bold, and add prefix
        if record.levelname in COLORS:
            color = COLORS[record.levelname]
            prefix = LEVEL_PREFIXES.get(record.levelname, '')
            record.levelname = f"{color}{COLORS['BOLD']}{prefix} {record.levelname}{COLORS['reset']}"
            
            # Format message with appropriate color
            if isinstance(record.msg, str):
                record.msg = f"{color}{record.msg}{COLORS['RESET']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_22(self, record):
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
                record.msg = None
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_23(self, record):
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
                record.msg = f"{color}{record.msg}{COLORS['XXRESETXX']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_24(self, record):
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
                record.msg = f"{color}{record.msg}{COLORS['reset']}"
        
        # Call the original formatter
        result = logging.Formatter.format(self, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_25(self, record):
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
        result = None
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_26(self, record):
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
        result = logging.Formatter.format(None, record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_27(self, record):
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
        result = logging.Formatter.format(self, None)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_28(self, record):
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
        result = logging.Formatter.format(record)
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_29(self, record):
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
        result = logging.Formatter.format(self, )
        
        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_30(self, record):
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
        record.levelname = None
        record.msg = orig_msg
        
        return result
    
    def xǁColoredFormatterǁformat__mutmut_31(self, record):
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
        record.msg = None
        
        return result
    
    xǁColoredFormatterǁformat__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁColoredFormatterǁformat__mutmut_1': xǁColoredFormatterǁformat__mutmut_1, 
        'xǁColoredFormatterǁformat__mutmut_2': xǁColoredFormatterǁformat__mutmut_2, 
        'xǁColoredFormatterǁformat__mutmut_3': xǁColoredFormatterǁformat__mutmut_3, 
        'xǁColoredFormatterǁformat__mutmut_4': xǁColoredFormatterǁformat__mutmut_4, 
        'xǁColoredFormatterǁformat__mutmut_5': xǁColoredFormatterǁformat__mutmut_5, 
        'xǁColoredFormatterǁformat__mutmut_6': xǁColoredFormatterǁformat__mutmut_6, 
        'xǁColoredFormatterǁformat__mutmut_7': xǁColoredFormatterǁformat__mutmut_7, 
        'xǁColoredFormatterǁformat__mutmut_8': xǁColoredFormatterǁformat__mutmut_8, 
        'xǁColoredFormatterǁformat__mutmut_9': xǁColoredFormatterǁformat__mutmut_9, 
        'xǁColoredFormatterǁformat__mutmut_10': xǁColoredFormatterǁformat__mutmut_10, 
        'xǁColoredFormatterǁformat__mutmut_11': xǁColoredFormatterǁformat__mutmut_11, 
        'xǁColoredFormatterǁformat__mutmut_12': xǁColoredFormatterǁformat__mutmut_12, 
        'xǁColoredFormatterǁformat__mutmut_13': xǁColoredFormatterǁformat__mutmut_13, 
        'xǁColoredFormatterǁformat__mutmut_14': xǁColoredFormatterǁformat__mutmut_14, 
        'xǁColoredFormatterǁformat__mutmut_15': xǁColoredFormatterǁformat__mutmut_15, 
        'xǁColoredFormatterǁformat__mutmut_16': xǁColoredFormatterǁformat__mutmut_16, 
        'xǁColoredFormatterǁformat__mutmut_17': xǁColoredFormatterǁformat__mutmut_17, 
        'xǁColoredFormatterǁformat__mutmut_18': xǁColoredFormatterǁformat__mutmut_18, 
        'xǁColoredFormatterǁformat__mutmut_19': xǁColoredFormatterǁformat__mutmut_19, 
        'xǁColoredFormatterǁformat__mutmut_20': xǁColoredFormatterǁformat__mutmut_20, 
        'xǁColoredFormatterǁformat__mutmut_21': xǁColoredFormatterǁformat__mutmut_21, 
        'xǁColoredFormatterǁformat__mutmut_22': xǁColoredFormatterǁformat__mutmut_22, 
        'xǁColoredFormatterǁformat__mutmut_23': xǁColoredFormatterǁformat__mutmut_23, 
        'xǁColoredFormatterǁformat__mutmut_24': xǁColoredFormatterǁformat__mutmut_24, 
        'xǁColoredFormatterǁformat__mutmut_25': xǁColoredFormatterǁformat__mutmut_25, 
        'xǁColoredFormatterǁformat__mutmut_26': xǁColoredFormatterǁformat__mutmut_26, 
        'xǁColoredFormatterǁformat__mutmut_27': xǁColoredFormatterǁformat__mutmut_27, 
        'xǁColoredFormatterǁformat__mutmut_28': xǁColoredFormatterǁformat__mutmut_28, 
        'xǁColoredFormatterǁformat__mutmut_29': xǁColoredFormatterǁformat__mutmut_29, 
        'xǁColoredFormatterǁformat__mutmut_30': xǁColoredFormatterǁformat__mutmut_30, 
        'xǁColoredFormatterǁformat__mutmut_31': xǁColoredFormatterǁformat__mutmut_31
    }
    
    def format(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁColoredFormatterǁformat__mutmut_orig"), object.__getattribute__(self, "xǁColoredFormatterǁformat__mutmut_mutants"), args, kwargs, self)
        return result 
    
    format.__signature__ = _mutmut_signature(xǁColoredFormatterǁformat__mutmut_orig)
    xǁColoredFormatterǁformat__mutmut_orig.__name__ = 'xǁColoredFormatterǁformat'

# Configure logging
logger = logging.getLogger("liteagent")
logger.setLevel(logging.INFO)

# Console handler with colored output
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s \t| %(message)s'))
logger.addHandler(_console_handler)

def x_setup_logging__mutmut_orig(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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

def x_setup_logging__mutmut_1(log_level="XXINFOXX", log_to_file=False, log_file=None, use_colors=True):
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

def x_setup_logging__mutmut_2(log_level="info", log_to_file=False, log_file=None, use_colors=True):
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

def x_setup_logging__mutmut_3(log_level="INFO", log_to_file=True, log_file=None, use_colors=True):
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

def x_setup_logging__mutmut_4(log_level="INFO", log_to_file=False, log_file=None, use_colors=False):
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

def x_setup_logging__mutmut_5(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = None
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

def x_setup_logging__mutmut_6(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(None, log_level.upper(), logging.INFO)
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

def x_setup_logging__mutmut_7(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, None, logging.INFO)
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

def x_setup_logging__mutmut_8(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, log_level.upper(), None)
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

def x_setup_logging__mutmut_9(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(log_level.upper(), logging.INFO)
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

def x_setup_logging__mutmut_10(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, logging.INFO)
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

def x_setup_logging__mutmut_11(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, log_level.upper(), )
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

def x_setup_logging__mutmut_12(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
    """
    Set up logging for LiteAgent.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to a file
        log_file (str): Path to log file. If None, a default filename will be used
        use_colors (bool): Whether to use colored output in the console
    """
    # Set log level
    level = getattr(logging, log_level.lower(), logging.INFO)
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

def x_setup_logging__mutmut_13(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
    logger.setLevel(None)
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

def x_setup_logging__mutmut_14(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
    _console_handler.setLevel(None)
    
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

def x_setup_logging__mutmut_15(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            logger.removeHandler(None)
    
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

def x_setup_logging__mutmut_16(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(None)
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

def x_setup_logging__mutmut_17(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(ColoredFormatter(None))
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

def x_setup_logging__mutmut_18(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(ColoredFormatter('XX%(asctime)s | %(levelname)s \t| %(message)sXX'))
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

def x_setup_logging__mutmut_19(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(ColoredFormatter('%(ASCTIME)S | %(LEVELNAME)S \t| %(MESSAGE)S'))
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

def x_setup_logging__mutmut_20(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(None)
    
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

def x_setup_logging__mutmut_21(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(logging.Formatter(None))
    
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

def x_setup_logging__mutmut_22(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(logging.Formatter('XX%(asctime)s | %(levelname)s \t| %(message)sXX'))
    
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

def x_setup_logging__mutmut_23(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        _console_handler.setFormatter(logging.Formatter('%(ASCTIME)S | %(LEVELNAME)S \t| %(MESSAGE)S'))
    
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

def x_setup_logging__mutmut_24(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        if log_file is not None:
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

def x_setup_logging__mutmut_25(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            log_file = None
        
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

def x_setup_logging__mutmut_26(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            log_file = f"liteagent_{datetime.now().strftime(None)}.log"
        
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

def x_setup_logging__mutmut_27(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            log_file = f"liteagent_{datetime.now().strftime('XX%Y%m%d_%H%M%SXX')}.log"
        
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

def x_setup_logging__mutmut_28(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            log_file = f"liteagent_{datetime.now().strftime('%y%m%d_%h%m%s')}.log"
        
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

def x_setup_logging__mutmut_29(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            log_file = f"liteagent_{datetime.now().strftime('%Y%M%D_%H%M%S')}.log"
        
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

def x_setup_logging__mutmut_30(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        
        file_handler = None
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

def x_setup_logging__mutmut_31(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        
        file_handler = logging.FileHandler(None)
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

def x_setup_logging__mutmut_32(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        file_handler.setLevel(None)
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

def x_setup_logging__mutmut_33(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        file_handler.setFormatter(None)
        logger.addHandler(file_handler)
        
    logger.debug(f"Logging initialized at level {log_level}")
    
    # Log examples of each level to demonstrate colors if in debug mode
    if use_colors and level <= logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_34(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            None
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

def x_setup_logging__mutmut_35(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            'XX%(asctime)s | %(levelname)s | %(message)sXX'
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

def x_setup_logging__mutmut_36(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
            '%(ASCTIME)S | %(LEVELNAME)S | %(MESSAGE)S'
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

def x_setup_logging__mutmut_37(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.addHandler(None)
        
    logger.debug(f"Logging initialized at level {log_level}")
    
    # Log examples of each level to demonstrate colors if in debug mode
    if use_colors and level <= logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_38(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        
    logger.debug(None)
    
    # Log examples of each level to demonstrate colors if in debug mode
    if use_colors and level <= logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_39(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
    if use_colors or level <= logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_40(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
    if use_colors and level < logging.DEBUG:
        logger.debug("This is a DEBUG message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_41(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.debug(None)
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_42(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.debug("XXThis is a DEBUG message exampleXX")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_43(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.debug("this is a debug message example")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_44(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.debug("THIS IS A DEBUG MESSAGE EXAMPLE")
        logger.info("This is an INFO message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_45(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.info(None)
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_46(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.info("XXThis is an INFO message exampleXX")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_47(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.info("this is an info message example")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_48(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.info("THIS IS AN INFO MESSAGE EXAMPLE")
        logger.warning("This is a WARNING message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_49(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.warning(None)
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_50(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.warning("XXThis is a WARNING message exampleXX")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_51(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.warning("this is a warning message example")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_52(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.warning("THIS IS A WARNING MESSAGE EXAMPLE")
        logger.error("This is an ERROR message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_53(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.error(None)
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_54(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.error("XXThis is an ERROR message exampleXX")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_55(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.error("this is an error message example")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_56(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.error("THIS IS AN ERROR MESSAGE EXAMPLE")
        logger.critical("This is a CRITICAL message example")

def x_setup_logging__mutmut_57(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.critical(None)

def x_setup_logging__mutmut_58(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.critical("XXThis is a CRITICAL message exampleXX")

def x_setup_logging__mutmut_59(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.critical("this is a critical message example")

def x_setup_logging__mutmut_60(log_level="INFO", log_to_file=False, log_file=None, use_colors=True):
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
        logger.critical("THIS IS A CRITICAL MESSAGE EXAMPLE")

x_setup_logging__mutmut_mutants : ClassVar[MutantDict] = {
'x_setup_logging__mutmut_1': x_setup_logging__mutmut_1, 
    'x_setup_logging__mutmut_2': x_setup_logging__mutmut_2, 
    'x_setup_logging__mutmut_3': x_setup_logging__mutmut_3, 
    'x_setup_logging__mutmut_4': x_setup_logging__mutmut_4, 
    'x_setup_logging__mutmut_5': x_setup_logging__mutmut_5, 
    'x_setup_logging__mutmut_6': x_setup_logging__mutmut_6, 
    'x_setup_logging__mutmut_7': x_setup_logging__mutmut_7, 
    'x_setup_logging__mutmut_8': x_setup_logging__mutmut_8, 
    'x_setup_logging__mutmut_9': x_setup_logging__mutmut_9, 
    'x_setup_logging__mutmut_10': x_setup_logging__mutmut_10, 
    'x_setup_logging__mutmut_11': x_setup_logging__mutmut_11, 
    'x_setup_logging__mutmut_12': x_setup_logging__mutmut_12, 
    'x_setup_logging__mutmut_13': x_setup_logging__mutmut_13, 
    'x_setup_logging__mutmut_14': x_setup_logging__mutmut_14, 
    'x_setup_logging__mutmut_15': x_setup_logging__mutmut_15, 
    'x_setup_logging__mutmut_16': x_setup_logging__mutmut_16, 
    'x_setup_logging__mutmut_17': x_setup_logging__mutmut_17, 
    'x_setup_logging__mutmut_18': x_setup_logging__mutmut_18, 
    'x_setup_logging__mutmut_19': x_setup_logging__mutmut_19, 
    'x_setup_logging__mutmut_20': x_setup_logging__mutmut_20, 
    'x_setup_logging__mutmut_21': x_setup_logging__mutmut_21, 
    'x_setup_logging__mutmut_22': x_setup_logging__mutmut_22, 
    'x_setup_logging__mutmut_23': x_setup_logging__mutmut_23, 
    'x_setup_logging__mutmut_24': x_setup_logging__mutmut_24, 
    'x_setup_logging__mutmut_25': x_setup_logging__mutmut_25, 
    'x_setup_logging__mutmut_26': x_setup_logging__mutmut_26, 
    'x_setup_logging__mutmut_27': x_setup_logging__mutmut_27, 
    'x_setup_logging__mutmut_28': x_setup_logging__mutmut_28, 
    'x_setup_logging__mutmut_29': x_setup_logging__mutmut_29, 
    'x_setup_logging__mutmut_30': x_setup_logging__mutmut_30, 
    'x_setup_logging__mutmut_31': x_setup_logging__mutmut_31, 
    'x_setup_logging__mutmut_32': x_setup_logging__mutmut_32, 
    'x_setup_logging__mutmut_33': x_setup_logging__mutmut_33, 
    'x_setup_logging__mutmut_34': x_setup_logging__mutmut_34, 
    'x_setup_logging__mutmut_35': x_setup_logging__mutmut_35, 
    'x_setup_logging__mutmut_36': x_setup_logging__mutmut_36, 
    'x_setup_logging__mutmut_37': x_setup_logging__mutmut_37, 
    'x_setup_logging__mutmut_38': x_setup_logging__mutmut_38, 
    'x_setup_logging__mutmut_39': x_setup_logging__mutmut_39, 
    'x_setup_logging__mutmut_40': x_setup_logging__mutmut_40, 
    'x_setup_logging__mutmut_41': x_setup_logging__mutmut_41, 
    'x_setup_logging__mutmut_42': x_setup_logging__mutmut_42, 
    'x_setup_logging__mutmut_43': x_setup_logging__mutmut_43, 
    'x_setup_logging__mutmut_44': x_setup_logging__mutmut_44, 
    'x_setup_logging__mutmut_45': x_setup_logging__mutmut_45, 
    'x_setup_logging__mutmut_46': x_setup_logging__mutmut_46, 
    'x_setup_logging__mutmut_47': x_setup_logging__mutmut_47, 
    'x_setup_logging__mutmut_48': x_setup_logging__mutmut_48, 
    'x_setup_logging__mutmut_49': x_setup_logging__mutmut_49, 
    'x_setup_logging__mutmut_50': x_setup_logging__mutmut_50, 
    'x_setup_logging__mutmut_51': x_setup_logging__mutmut_51, 
    'x_setup_logging__mutmut_52': x_setup_logging__mutmut_52, 
    'x_setup_logging__mutmut_53': x_setup_logging__mutmut_53, 
    'x_setup_logging__mutmut_54': x_setup_logging__mutmut_54, 
    'x_setup_logging__mutmut_55': x_setup_logging__mutmut_55, 
    'x_setup_logging__mutmut_56': x_setup_logging__mutmut_56, 
    'x_setup_logging__mutmut_57': x_setup_logging__mutmut_57, 
    'x_setup_logging__mutmut_58': x_setup_logging__mutmut_58, 
    'x_setup_logging__mutmut_59': x_setup_logging__mutmut_59, 
    'x_setup_logging__mutmut_60': x_setup_logging__mutmut_60
}

def setup_logging(*args, **kwargs):
    result = _mutmut_trampoline(x_setup_logging__mutmut_orig, x_setup_logging__mutmut_mutants, args, kwargs)
    return result 

setup_logging.__signature__ = _mutmut_signature(x_setup_logging__mutmut_orig)
x_setup_logging__mutmut_orig.__name__ = 'x_setup_logging'

def x_log_completion_request__mutmut_orig(model, messages, functions=None, **kwargs):
    """Log a completion request in a structured format."""
    logger.debug(
        f"Request: model={model}, messages={len(messages)} messages, "
        f"functions={len(functions) if functions else 0}"
    )

def x_log_completion_request__mutmut_1(model, messages, functions=None, **kwargs):
    """Log a completion request in a structured format."""
    logger.debug(
        None
    )

def x_log_completion_request__mutmut_2(model, messages, functions=None, **kwargs):
    """Log a completion request in a structured format."""
    logger.debug(
        f"Request: model={model}, messages={len(messages)} messages, "
        f"functions={len(functions) if functions else 1}"
    )

x_log_completion_request__mutmut_mutants : ClassVar[MutantDict] = {
'x_log_completion_request__mutmut_1': x_log_completion_request__mutmut_1, 
    'x_log_completion_request__mutmut_2': x_log_completion_request__mutmut_2
}

def log_completion_request(*args, **kwargs):
    result = _mutmut_trampoline(x_log_completion_request__mutmut_orig, x_log_completion_request__mutmut_mutants, args, kwargs)
    return result 

log_completion_request.__signature__ = _mutmut_signature(x_log_completion_request__mutmut_orig)
x_log_completion_request__mutmut_orig.__name__ = 'x_log_completion_request'

def x_log_completion_response__mutmut_orig(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_1(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') or len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_2(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(None, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_3(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, None) and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_4(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr('choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_5(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, ) and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_6(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'XXchoicesXX') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_7(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'CHOICES') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_8(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) >= 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_9(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 1:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_10(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = None
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_11(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[1].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_12(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            None
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_13(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get(None, 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_14(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', None)}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_15(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_16(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', )}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_17(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(None, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_18(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, None, {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_19(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', None).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_20(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr('usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_21(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_22(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', ).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_23(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'XXusageXX', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_24(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'USAGE', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_25(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('XXtotal_tokensXX', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_26(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('TOTAL_TOKENS', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_27(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'XXunknownXX')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_28(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'UNKNOWN')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_29(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency and 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_30(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'XXunknownXX'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_31(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'UNKNOWN'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_32(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(None)

def x_log_completion_response__mutmut_33(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(None)}, latency={latency or 'unknown'} s")

def x_log_completion_response__mutmut_34(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency and 'unknown'} s")

def x_log_completion_response__mutmut_35(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'XXunknownXX'} s")

def x_log_completion_response__mutmut_36(response, latency=None):
    """Log a completion response in a structured format."""
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message
        logger.debug(
            f"Response: tokens={getattr(response, 'usage', {}).get('total_tokens', 'unknown')}, "
            f"latency={latency or 'unknown'} s"
        )
    else:
        logger.debug(f"Response: {type(response)}, latency={latency or 'UNKNOWN'} s")

x_log_completion_response__mutmut_mutants : ClassVar[MutantDict] = {
'x_log_completion_response__mutmut_1': x_log_completion_response__mutmut_1, 
    'x_log_completion_response__mutmut_2': x_log_completion_response__mutmut_2, 
    'x_log_completion_response__mutmut_3': x_log_completion_response__mutmut_3, 
    'x_log_completion_response__mutmut_4': x_log_completion_response__mutmut_4, 
    'x_log_completion_response__mutmut_5': x_log_completion_response__mutmut_5, 
    'x_log_completion_response__mutmut_6': x_log_completion_response__mutmut_6, 
    'x_log_completion_response__mutmut_7': x_log_completion_response__mutmut_7, 
    'x_log_completion_response__mutmut_8': x_log_completion_response__mutmut_8, 
    'x_log_completion_response__mutmut_9': x_log_completion_response__mutmut_9, 
    'x_log_completion_response__mutmut_10': x_log_completion_response__mutmut_10, 
    'x_log_completion_response__mutmut_11': x_log_completion_response__mutmut_11, 
    'x_log_completion_response__mutmut_12': x_log_completion_response__mutmut_12, 
    'x_log_completion_response__mutmut_13': x_log_completion_response__mutmut_13, 
    'x_log_completion_response__mutmut_14': x_log_completion_response__mutmut_14, 
    'x_log_completion_response__mutmut_15': x_log_completion_response__mutmut_15, 
    'x_log_completion_response__mutmut_16': x_log_completion_response__mutmut_16, 
    'x_log_completion_response__mutmut_17': x_log_completion_response__mutmut_17, 
    'x_log_completion_response__mutmut_18': x_log_completion_response__mutmut_18, 
    'x_log_completion_response__mutmut_19': x_log_completion_response__mutmut_19, 
    'x_log_completion_response__mutmut_20': x_log_completion_response__mutmut_20, 
    'x_log_completion_response__mutmut_21': x_log_completion_response__mutmut_21, 
    'x_log_completion_response__mutmut_22': x_log_completion_response__mutmut_22, 
    'x_log_completion_response__mutmut_23': x_log_completion_response__mutmut_23, 
    'x_log_completion_response__mutmut_24': x_log_completion_response__mutmut_24, 
    'x_log_completion_response__mutmut_25': x_log_completion_response__mutmut_25, 
    'x_log_completion_response__mutmut_26': x_log_completion_response__mutmut_26, 
    'x_log_completion_response__mutmut_27': x_log_completion_response__mutmut_27, 
    'x_log_completion_response__mutmut_28': x_log_completion_response__mutmut_28, 
    'x_log_completion_response__mutmut_29': x_log_completion_response__mutmut_29, 
    'x_log_completion_response__mutmut_30': x_log_completion_response__mutmut_30, 
    'x_log_completion_response__mutmut_31': x_log_completion_response__mutmut_31, 
    'x_log_completion_response__mutmut_32': x_log_completion_response__mutmut_32, 
    'x_log_completion_response__mutmut_33': x_log_completion_response__mutmut_33, 
    'x_log_completion_response__mutmut_34': x_log_completion_response__mutmut_34, 
    'x_log_completion_response__mutmut_35': x_log_completion_response__mutmut_35, 
    'x_log_completion_response__mutmut_36': x_log_completion_response__mutmut_36
}

def log_completion_response(*args, **kwargs):
    result = _mutmut_trampoline(x_log_completion_response__mutmut_orig, x_log_completion_response__mutmut_mutants, args, kwargs)
    return result 

log_completion_response.__signature__ = _mutmut_signature(x_log_completion_response__mutmut_orig)
x_log_completion_response__mutmut_orig.__name__ = 'x_log_completion_response'

def x_check_api_keys__mutmut_orig():
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

def x_check_api_keys__mutmut_1():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info(None)
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

def x_check_api_keys__mutmut_2():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("XXChecking for API keys...XX")
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

def x_check_api_keys__mutmut_3():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("checking for api keys...")
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

def x_check_api_keys__mutmut_4():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("CHECKING FOR API KEYS...")
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

def x_check_api_keys__mutmut_5():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = None
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_6():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "XXOPENAI_API_KEYXX": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_7():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "openai_api_key": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_8():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "XXOPENAI_API_KEYXX" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_9():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "openai_api_key" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_10():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" not in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_11():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "XXLITELLM_API_KEYXX": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_12():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "litellm_api_key": "LITELLM_API_KEY" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_13():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "XXLITELLM_API_KEYXX" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_14():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "litellm_api_key" in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_15():
    """
    Check if required API keys are present in the environment.
    
    Returns:
        dict: A dictionary of API key statuses
    """
    logger.info("Checking for API keys...")
    keys = {
        "OPENAI_API_KEY": "OPENAI_API_KEY" in os.environ,
        "LITELLM_API_KEY": "LITELLM_API_KEY" not in os.environ
    }
    
    for key, present in keys.items():
        status = "✓" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_16():
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
        status = None
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_17():
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
        status = "XX✓XX" if present else "✗"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_18():
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
        status = "✓" if present else "XX✗XX"
        if present:
            logger.info(f"{status} {key} found")
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_19():
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
            logger.info(None)
        else:
            logger.warning(f"{status} {key} found")
        
    return keys

def x_check_api_keys__mutmut_20():
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
            logger.warning(None)
        
    return keys

x_check_api_keys__mutmut_mutants : ClassVar[MutantDict] = {
'x_check_api_keys__mutmut_1': x_check_api_keys__mutmut_1, 
    'x_check_api_keys__mutmut_2': x_check_api_keys__mutmut_2, 
    'x_check_api_keys__mutmut_3': x_check_api_keys__mutmut_3, 
    'x_check_api_keys__mutmut_4': x_check_api_keys__mutmut_4, 
    'x_check_api_keys__mutmut_5': x_check_api_keys__mutmut_5, 
    'x_check_api_keys__mutmut_6': x_check_api_keys__mutmut_6, 
    'x_check_api_keys__mutmut_7': x_check_api_keys__mutmut_7, 
    'x_check_api_keys__mutmut_8': x_check_api_keys__mutmut_8, 
    'x_check_api_keys__mutmut_9': x_check_api_keys__mutmut_9, 
    'x_check_api_keys__mutmut_10': x_check_api_keys__mutmut_10, 
    'x_check_api_keys__mutmut_11': x_check_api_keys__mutmut_11, 
    'x_check_api_keys__mutmut_12': x_check_api_keys__mutmut_12, 
    'x_check_api_keys__mutmut_13': x_check_api_keys__mutmut_13, 
    'x_check_api_keys__mutmut_14': x_check_api_keys__mutmut_14, 
    'x_check_api_keys__mutmut_15': x_check_api_keys__mutmut_15, 
    'x_check_api_keys__mutmut_16': x_check_api_keys__mutmut_16, 
    'x_check_api_keys__mutmut_17': x_check_api_keys__mutmut_17, 
    'x_check_api_keys__mutmut_18': x_check_api_keys__mutmut_18, 
    'x_check_api_keys__mutmut_19': x_check_api_keys__mutmut_19, 
    'x_check_api_keys__mutmut_20': x_check_api_keys__mutmut_20
}

def check_api_keys(*args, **kwargs):
    result = _mutmut_trampoline(x_check_api_keys__mutmut_orig, x_check_api_keys__mutmut_mutants, args, kwargs)
    return result 

check_api_keys.__signature__ = _mutmut_signature(x_check_api_keys__mutmut_orig)
x_check_api_keys__mutmut_orig.__name__ = 'x_check_api_keys'

def x_safe_json_serialize__mutmut_orig(obj):
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

def x_safe_json_serialize__mutmut_1(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(None, indent=2)
    except (TypeError, ValueError):
        return str(obj)

def x_safe_json_serialize__mutmut_2(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(obj, indent=None)
    except (TypeError, ValueError):
        return str(obj)

def x_safe_json_serialize__mutmut_3(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(indent=2)
    except (TypeError, ValueError):
        return str(obj)

def x_safe_json_serialize__mutmut_4(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(obj, )
    except (TypeError, ValueError):
        return str(obj)

def x_safe_json_serialize__mutmut_5(obj):
    """
    Safely serialize an object to JSON.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON string or string representation of the object if serialization fails
    """
    try:
        return json.dumps(obj, indent=3)
    except (TypeError, ValueError):
        return str(obj)

def x_safe_json_serialize__mutmut_6(obj):
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
        return str(None)

x_safe_json_serialize__mutmut_mutants : ClassVar[MutantDict] = {
'x_safe_json_serialize__mutmut_1': x_safe_json_serialize__mutmut_1, 
    'x_safe_json_serialize__mutmut_2': x_safe_json_serialize__mutmut_2, 
    'x_safe_json_serialize__mutmut_3': x_safe_json_serialize__mutmut_3, 
    'x_safe_json_serialize__mutmut_4': x_safe_json_serialize__mutmut_4, 
    'x_safe_json_serialize__mutmut_5': x_safe_json_serialize__mutmut_5, 
    'x_safe_json_serialize__mutmut_6': x_safe_json_serialize__mutmut_6
}

def safe_json_serialize(*args, **kwargs):
    result = _mutmut_trampoline(x_safe_json_serialize__mutmut_orig, x_safe_json_serialize__mutmut_mutants, args, kwargs)
    return result 

safe_json_serialize.__signature__ = _mutmut_signature(x_safe_json_serialize__mutmut_orig)
x_safe_json_serialize__mutmut_orig.__name__ = 'x_safe_json_serialize'