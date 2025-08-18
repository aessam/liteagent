"""
Tool calling utilities and tracking.

This module provides utilities for tracking and managing tool calls.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time
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


@dataclass
class ToolCallRecord:
    """Record of a tool call execution."""
    name: str
    arguments: Dict[str, Any]
    result: Any
    timestamp: float
    execution_time: Optional[float] = None
    error: Optional[str] = None


class ToolCallTracker:
    """Tracks tool calls for debugging and analysis."""
    
    _instance = None
    
    def xǁToolCallTrackerǁ__init____mutmut_orig(self):
        """Initialize the tool call tracker."""
        self.calls: List[ToolCallRecord] = []
        self._call_counts: Dict[str, int] = {}
    
    def xǁToolCallTrackerǁ__init____mutmut_1(self):
        """Initialize the tool call tracker."""
        self.calls: List[ToolCallRecord] = None
        self._call_counts: Dict[str, int] = {}
    
    def xǁToolCallTrackerǁ__init____mutmut_2(self):
        """Initialize the tool call tracker."""
        self.calls: List[ToolCallRecord] = []
        self._call_counts: Dict[str, int] = None
    
    xǁToolCallTrackerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁ__init____mutmut_1': xǁToolCallTrackerǁ__init____mutmut_1, 
        'xǁToolCallTrackerǁ__init____mutmut_2': xǁToolCallTrackerǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁToolCallTrackerǁ__init____mutmut_orig)
    xǁToolCallTrackerǁ__init____mutmut_orig.__name__ = 'xǁToolCallTrackerǁ__init__'
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of ToolCallTracker."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def xǁToolCallTrackerǁrecord_call__mutmut_orig(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_1(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = None
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_2(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=None,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_3(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=None,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_4(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=None,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_5(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=None,
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_6(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=None,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_7(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=None
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_8(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_9(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_10(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_11(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_12(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_13(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_14(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(None)
        self._call_counts[name] = self._call_counts.get(name, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_15(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = None
    
    def xǁToolCallTrackerǁrecord_call__mutmut_16(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) - 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_17(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(None, 0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_18(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, None) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_19(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(0) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_20(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, ) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_21(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 1) + 1
    
    def xǁToolCallTrackerǁrecord_call__mutmut_22(self, name: str, arguments: Dict[str, Any], result: Any = None, 
                   execution_time: Optional[float] = None, error: Optional[str] = None) -> None:
        """
        Record a tool call.
        
        Args:
            name: Name of the tool
            arguments: Arguments passed to the tool
            result: Result of the tool call
            execution_time: Time taken to execute the tool
            error: Error message if the call failed
        """
        record = ToolCallRecord(
            name=name,
            arguments=arguments,
            result=result,
            timestamp=time.time(),
            execution_time=execution_time,
            error=error
        )
        
        self.calls.append(record)
        self._call_counts[name] = self._call_counts.get(name, 0) + 2
    
    xǁToolCallTrackerǁrecord_call__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁrecord_call__mutmut_1': xǁToolCallTrackerǁrecord_call__mutmut_1, 
        'xǁToolCallTrackerǁrecord_call__mutmut_2': xǁToolCallTrackerǁrecord_call__mutmut_2, 
        'xǁToolCallTrackerǁrecord_call__mutmut_3': xǁToolCallTrackerǁrecord_call__mutmut_3, 
        'xǁToolCallTrackerǁrecord_call__mutmut_4': xǁToolCallTrackerǁrecord_call__mutmut_4, 
        'xǁToolCallTrackerǁrecord_call__mutmut_5': xǁToolCallTrackerǁrecord_call__mutmut_5, 
        'xǁToolCallTrackerǁrecord_call__mutmut_6': xǁToolCallTrackerǁrecord_call__mutmut_6, 
        'xǁToolCallTrackerǁrecord_call__mutmut_7': xǁToolCallTrackerǁrecord_call__mutmut_7, 
        'xǁToolCallTrackerǁrecord_call__mutmut_8': xǁToolCallTrackerǁrecord_call__mutmut_8, 
        'xǁToolCallTrackerǁrecord_call__mutmut_9': xǁToolCallTrackerǁrecord_call__mutmut_9, 
        'xǁToolCallTrackerǁrecord_call__mutmut_10': xǁToolCallTrackerǁrecord_call__mutmut_10, 
        'xǁToolCallTrackerǁrecord_call__mutmut_11': xǁToolCallTrackerǁrecord_call__mutmut_11, 
        'xǁToolCallTrackerǁrecord_call__mutmut_12': xǁToolCallTrackerǁrecord_call__mutmut_12, 
        'xǁToolCallTrackerǁrecord_call__mutmut_13': xǁToolCallTrackerǁrecord_call__mutmut_13, 
        'xǁToolCallTrackerǁrecord_call__mutmut_14': xǁToolCallTrackerǁrecord_call__mutmut_14, 
        'xǁToolCallTrackerǁrecord_call__mutmut_15': xǁToolCallTrackerǁrecord_call__mutmut_15, 
        'xǁToolCallTrackerǁrecord_call__mutmut_16': xǁToolCallTrackerǁrecord_call__mutmut_16, 
        'xǁToolCallTrackerǁrecord_call__mutmut_17': xǁToolCallTrackerǁrecord_call__mutmut_17, 
        'xǁToolCallTrackerǁrecord_call__mutmut_18': xǁToolCallTrackerǁrecord_call__mutmut_18, 
        'xǁToolCallTrackerǁrecord_call__mutmut_19': xǁToolCallTrackerǁrecord_call__mutmut_19, 
        'xǁToolCallTrackerǁrecord_call__mutmut_20': xǁToolCallTrackerǁrecord_call__mutmut_20, 
        'xǁToolCallTrackerǁrecord_call__mutmut_21': xǁToolCallTrackerǁrecord_call__mutmut_21, 
        'xǁToolCallTrackerǁrecord_call__mutmut_22': xǁToolCallTrackerǁrecord_call__mutmut_22
    }
    
    def record_call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁrecord_call__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁrecord_call__mutmut_mutants"), args, kwargs, self)
        return result 
    
    record_call.__signature__ = _mutmut_signature(xǁToolCallTrackerǁrecord_call__mutmut_orig)
    xǁToolCallTrackerǁrecord_call__mutmut_orig.__name__ = 'xǁToolCallTrackerǁrecord_call'
    
    def xǁToolCallTrackerǁget_call_count__mutmut_orig(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(tool_name, 0)
    
    def xǁToolCallTrackerǁget_call_count__mutmut_1(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(None, 0)
    
    def xǁToolCallTrackerǁget_call_count__mutmut_2(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(tool_name, None)
    
    def xǁToolCallTrackerǁget_call_count__mutmut_3(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(0)
    
    def xǁToolCallTrackerǁget_call_count__mutmut_4(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(tool_name, )
    
    def xǁToolCallTrackerǁget_call_count__mutmut_5(self, tool_name: str) -> int:
        """Get the number of times a tool was called."""
        return self._call_counts.get(tool_name, 1)
    
    xǁToolCallTrackerǁget_call_count__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁget_call_count__mutmut_1': xǁToolCallTrackerǁget_call_count__mutmut_1, 
        'xǁToolCallTrackerǁget_call_count__mutmut_2': xǁToolCallTrackerǁget_call_count__mutmut_2, 
        'xǁToolCallTrackerǁget_call_count__mutmut_3': xǁToolCallTrackerǁget_call_count__mutmut_3, 
        'xǁToolCallTrackerǁget_call_count__mutmut_4': xǁToolCallTrackerǁget_call_count__mutmut_4, 
        'xǁToolCallTrackerǁget_call_count__mutmut_5': xǁToolCallTrackerǁget_call_count__mutmut_5
    }
    
    def get_call_count(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁget_call_count__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁget_call_count__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_call_count.__signature__ = _mutmut_signature(xǁToolCallTrackerǁget_call_count__mutmut_orig)
    xǁToolCallTrackerǁget_call_count__mutmut_orig.__name__ = 'xǁToolCallTrackerǁget_call_count'
    
    def xǁToolCallTrackerǁwas_tool_called__mutmut_orig(self, tool_name: str) -> bool:
        """Check if a tool was called at least once."""
        return self.get_call_count(tool_name) > 0
    
    def xǁToolCallTrackerǁwas_tool_called__mutmut_1(self, tool_name: str) -> bool:
        """Check if a tool was called at least once."""
        return self.get_call_count(None) > 0
    
    def xǁToolCallTrackerǁwas_tool_called__mutmut_2(self, tool_name: str) -> bool:
        """Check if a tool was called at least once."""
        return self.get_call_count(tool_name) >= 0
    
    def xǁToolCallTrackerǁwas_tool_called__mutmut_3(self, tool_name: str) -> bool:
        """Check if a tool was called at least once."""
        return self.get_call_count(tool_name) > 1
    
    xǁToolCallTrackerǁwas_tool_called__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁwas_tool_called__mutmut_1': xǁToolCallTrackerǁwas_tool_called__mutmut_1, 
        'xǁToolCallTrackerǁwas_tool_called__mutmut_2': xǁToolCallTrackerǁwas_tool_called__mutmut_2, 
        'xǁToolCallTrackerǁwas_tool_called__mutmut_3': xǁToolCallTrackerǁwas_tool_called__mutmut_3
    }
    
    def was_tool_called(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁwas_tool_called__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁwas_tool_called__mutmut_mutants"), args, kwargs, self)
        return result 
    
    was_tool_called.__signature__ = _mutmut_signature(xǁToolCallTrackerǁwas_tool_called__mutmut_orig)
    xǁToolCallTrackerǁwas_tool_called__mutmut_orig.__name__ = 'xǁToolCallTrackerǁwas_tool_called'
    
    def xǁToolCallTrackerǁget_calls_for_tool__mutmut_orig(self, tool_name: str) -> List[ToolCallRecord]:
        """Get all calls for a specific tool."""
        return [call for call in self.calls if call.name == tool_name]
    
    def xǁToolCallTrackerǁget_calls_for_tool__mutmut_1(self, tool_name: str) -> List[ToolCallRecord]:
        """Get all calls for a specific tool."""
        return [call for call in self.calls if call.name != tool_name]
    
    xǁToolCallTrackerǁget_calls_for_tool__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁget_calls_for_tool__mutmut_1': xǁToolCallTrackerǁget_calls_for_tool__mutmut_1
    }
    
    def get_calls_for_tool(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁget_calls_for_tool__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁget_calls_for_tool__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_calls_for_tool.__signature__ = _mutmut_signature(xǁToolCallTrackerǁget_calls_for_tool__mutmut_orig)
    xǁToolCallTrackerǁget_calls_for_tool__mutmut_orig.__name__ = 'xǁToolCallTrackerǁget_calls_for_tool'
    
    def clear(self) -> None:
        """Clear all recorded calls."""
        self.calls.clear()
        self._call_counts.clear()
    
    def reset(self) -> None:
        """Reset the tracker (alias for clear)."""
        self.clear()
    
    @property
    def total_calls(self) -> int:
        """Get the total number of calls recorded."""
        return len(self.calls)
    
    @property
    def unique_tools_called(self) -> List[str]:
        """Get list of unique tool names that were called."""
        return list(self._call_counts.keys())
    
    def xǁToolCallTrackerǁget_tool_args__mutmut_orig(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the arguments from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dict containing the arguments, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[-1].arguments
        return None
    
    def xǁToolCallTrackerǁget_tool_args__mutmut_1(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the arguments from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dict containing the arguments, or None if tool wasn't called
        """
        calls = None
        if calls:
            return calls[-1].arguments
        return None
    
    def xǁToolCallTrackerǁget_tool_args__mutmut_2(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the arguments from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dict containing the arguments, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(None)
        if calls:
            return calls[-1].arguments
        return None
    
    def xǁToolCallTrackerǁget_tool_args__mutmut_3(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the arguments from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dict containing the arguments, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[+1].arguments
        return None
    
    def xǁToolCallTrackerǁget_tool_args__mutmut_4(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the arguments from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dict containing the arguments, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[-2].arguments
        return None
    
    xǁToolCallTrackerǁget_tool_args__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁget_tool_args__mutmut_1': xǁToolCallTrackerǁget_tool_args__mutmut_1, 
        'xǁToolCallTrackerǁget_tool_args__mutmut_2': xǁToolCallTrackerǁget_tool_args__mutmut_2, 
        'xǁToolCallTrackerǁget_tool_args__mutmut_3': xǁToolCallTrackerǁget_tool_args__mutmut_3, 
        'xǁToolCallTrackerǁget_tool_args__mutmut_4': xǁToolCallTrackerǁget_tool_args__mutmut_4
    }
    
    def get_tool_args(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁget_tool_args__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁget_tool_args__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_tool_args.__signature__ = _mutmut_signature(xǁToolCallTrackerǁget_tool_args__mutmut_orig)
    xǁToolCallTrackerǁget_tool_args__mutmut_orig.__name__ = 'xǁToolCallTrackerǁget_tool_args'
    
    def xǁToolCallTrackerǁget_tool_result__mutmut_orig(self, tool_name: str) -> Any:
        """
        Get the result from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            The result of the most recent call, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[-1].result
        return None
    
    def xǁToolCallTrackerǁget_tool_result__mutmut_1(self, tool_name: str) -> Any:
        """
        Get the result from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            The result of the most recent call, or None if tool wasn't called
        """
        calls = None
        if calls:
            return calls[-1].result
        return None
    
    def xǁToolCallTrackerǁget_tool_result__mutmut_2(self, tool_name: str) -> Any:
        """
        Get the result from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            The result of the most recent call, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(None)
        if calls:
            return calls[-1].result
        return None
    
    def xǁToolCallTrackerǁget_tool_result__mutmut_3(self, tool_name: str) -> Any:
        """
        Get the result from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            The result of the most recent call, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[+1].result
        return None
    
    def xǁToolCallTrackerǁget_tool_result__mutmut_4(self, tool_name: str) -> Any:
        """
        Get the result from the most recent call to a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            The result of the most recent call, or None if tool wasn't called
        """
        calls = self.get_calls_for_tool(tool_name)
        if calls:
            return calls[-2].result
        return None
    
    xǁToolCallTrackerǁget_tool_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolCallTrackerǁget_tool_result__mutmut_1': xǁToolCallTrackerǁget_tool_result__mutmut_1, 
        'xǁToolCallTrackerǁget_tool_result__mutmut_2': xǁToolCallTrackerǁget_tool_result__mutmut_2, 
        'xǁToolCallTrackerǁget_tool_result__mutmut_3': xǁToolCallTrackerǁget_tool_result__mutmut_3, 
        'xǁToolCallTrackerǁget_tool_result__mutmut_4': xǁToolCallTrackerǁget_tool_result__mutmut_4
    }
    
    def get_tool_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolCallTrackerǁget_tool_result__mutmut_orig"), object.__getattribute__(self, "xǁToolCallTrackerǁget_tool_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_tool_result.__signature__ = _mutmut_signature(xǁToolCallTrackerǁget_tool_result__mutmut_orig)
    xǁToolCallTrackerǁget_tool_result__mutmut_orig.__name__ = 'xǁToolCallTrackerǁget_tool_result'