"""
Compatibility module for tool calling types.

This module provides backward compatibility for tests that reference
the old tool calling type system.
"""

from enum import Enum
from typing import Optional
from .capabilities import get_model_capabilities
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


class ToolCallingType(Enum):
    """Enum representing different tool calling capabilities."""
    NONE = "none"
    BASIC = "basic"
    PARALLEL = "parallel"
    ADVANCED = "advanced"


def x_get_tool_calling_type__mutmut_orig(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(model_name)
    
    if not capabilities or not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC


def x_get_tool_calling_type__mutmut_1(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = None
    
    if not capabilities or not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC


def x_get_tool_calling_type__mutmut_2(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(None)
    
    if not capabilities or not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC


def x_get_tool_calling_type__mutmut_3(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(model_name)
    
    if not capabilities and not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC


def x_get_tool_calling_type__mutmut_4(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(model_name)
    
    if capabilities or not capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC


def x_get_tool_calling_type__mutmut_5(model_name) -> ToolCallingType:
    """
    Get the tool calling type for a given model.
    
    Args:
        model_name: Name of the model (string) or (provider, model) tuple
        
    Returns:
        ToolCallingType: The tool calling capability type
    """
    capabilities = get_model_capabilities(model_name)
    
    if not capabilities or capabilities.tool_calling:
        return ToolCallingType.NONE
    
    if capabilities.supports_parallel_tools:
        return ToolCallingType.PARALLEL
    
    # Default to basic tool calling if model supports tools
    return ToolCallingType.BASIC

x_get_tool_calling_type__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_tool_calling_type__mutmut_1': x_get_tool_calling_type__mutmut_1, 
    'x_get_tool_calling_type__mutmut_2': x_get_tool_calling_type__mutmut_2, 
    'x_get_tool_calling_type__mutmut_3': x_get_tool_calling_type__mutmut_3, 
    'x_get_tool_calling_type__mutmut_4': x_get_tool_calling_type__mutmut_4, 
    'x_get_tool_calling_type__mutmut_5': x_get_tool_calling_type__mutmut_5
}

def get_tool_calling_type(*args, **kwargs):
    result = _mutmut_trampoline(x_get_tool_calling_type__mutmut_orig, x_get_tool_calling_type__mutmut_mutants, args, kwargs)
    return result 

get_tool_calling_type.__signature__ = _mutmut_signature(x_get_tool_calling_type__mutmut_orig)
x_get_tool_calling_type__mutmut_orig.__name__ = 'x_get_tool_calling_type'