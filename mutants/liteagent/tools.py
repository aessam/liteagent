"""
Tool management module for LiteAgent.

This module provides functionality for registering and managing tools 
that can be used by the agent to perform various tasks.
"""

from pydantic import create_model, BaseModel
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union
import functools
import random

# Global registry for tools
TOOLS = {}
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

class ToolsForAgents:
    """
    A class containing tools that can be used by agents.
    
    DEPRECATED: This class has been moved to tests.utils.test_tools.ToolsForAgents as it
    is primarily intended for testing purposes. Use that version instead.
    """
    
    def xǁToolsForAgentsǁ__init____mutmut_orig(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_1(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            None,
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_2(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            None,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_3(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=None
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_4(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_5(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_6(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_7(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "XXToolsForAgents in the main library is deprecated and will be removed in a future version. XX"
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_8(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "toolsforagents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_9(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "TOOLSFORAGENTS IN THE MAIN LIBRARY IS DEPRECATED AND WILL BE REMOVED IN A FUTURE VERSION. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_10(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "XXImport it from tests.utils.test_tools instead.XX",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_11(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_12(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "IMPORT IT FROM TESTS.UTILS.TEST_TOOLS INSTEAD.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_13(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=3
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=api_key)
        
    
    def xǁToolsForAgentsǁ__init____mutmut_14(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = None
        
    
    def xǁToolsForAgentsǁ__init____mutmut_15(self, api_key=None):
        """Initialize with an optional API key."""
        import warnings
        warnings.warn(
            "ToolsForAgents in the main library is deprecated and will be removed in a future version. "
            "Import it from tests.utils.test_tools instead.",
            DeprecationWarning,
            stacklevel=2
        )
        from tests.utils.test_tools import ToolsForAgents as TestToolsForAgents
        self._instance = TestToolsForAgents(api_key=None)
        
    
    xǁToolsForAgentsǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolsForAgentsǁ__init____mutmut_1': xǁToolsForAgentsǁ__init____mutmut_1, 
        'xǁToolsForAgentsǁ__init____mutmut_2': xǁToolsForAgentsǁ__init____mutmut_2, 
        'xǁToolsForAgentsǁ__init____mutmut_3': xǁToolsForAgentsǁ__init____mutmut_3, 
        'xǁToolsForAgentsǁ__init____mutmut_4': xǁToolsForAgentsǁ__init____mutmut_4, 
        'xǁToolsForAgentsǁ__init____mutmut_5': xǁToolsForAgentsǁ__init____mutmut_5, 
        'xǁToolsForAgentsǁ__init____mutmut_6': xǁToolsForAgentsǁ__init____mutmut_6, 
        'xǁToolsForAgentsǁ__init____mutmut_7': xǁToolsForAgentsǁ__init____mutmut_7, 
        'xǁToolsForAgentsǁ__init____mutmut_8': xǁToolsForAgentsǁ__init____mutmut_8, 
        'xǁToolsForAgentsǁ__init____mutmut_9': xǁToolsForAgentsǁ__init____mutmut_9, 
        'xǁToolsForAgentsǁ__init____mutmut_10': xǁToolsForAgentsǁ__init____mutmut_10, 
        'xǁToolsForAgentsǁ__init____mutmut_11': xǁToolsForAgentsǁ__init____mutmut_11, 
        'xǁToolsForAgentsǁ__init____mutmut_12': xǁToolsForAgentsǁ__init____mutmut_12, 
        'xǁToolsForAgentsǁ__init____mutmut_13': xǁToolsForAgentsǁ__init____mutmut_13, 
        'xǁToolsForAgentsǁ__init____mutmut_14': xǁToolsForAgentsǁ__init____mutmut_14, 
        'xǁToolsForAgentsǁ__init____mutmut_15': xǁToolsForAgentsǁ__init____mutmut_15
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolsForAgentsǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁToolsForAgentsǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁToolsForAgentsǁ__init____mutmut_orig)
    xǁToolsForAgentsǁ__init____mutmut_orig.__name__ = 'xǁToolsForAgentsǁ__init__'
    def xǁToolsForAgentsǁadd_numbers__mutmut_orig(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(a, b)
        
    def xǁToolsForAgentsǁadd_numbers__mutmut_1(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(None, b)
        
    def xǁToolsForAgentsǁadd_numbers__mutmut_2(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(a, None)
        
    def xǁToolsForAgentsǁadd_numbers__mutmut_3(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(b)
        
    def xǁToolsForAgentsǁadd_numbers__mutmut_4(self, a: int, b: int) -> int:
        """Adds two numbers together."""
        return self._instance.add_numbers(a, )
        
    
    xǁToolsForAgentsǁadd_numbers__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolsForAgentsǁadd_numbers__mutmut_1': xǁToolsForAgentsǁadd_numbers__mutmut_1, 
        'xǁToolsForAgentsǁadd_numbers__mutmut_2': xǁToolsForAgentsǁadd_numbers__mutmut_2, 
        'xǁToolsForAgentsǁadd_numbers__mutmut_3': xǁToolsForAgentsǁadd_numbers__mutmut_3, 
        'xǁToolsForAgentsǁadd_numbers__mutmut_4': xǁToolsForAgentsǁadd_numbers__mutmut_4
    }
    
    def add_numbers(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolsForAgentsǁadd_numbers__mutmut_orig"), object.__getattribute__(self, "xǁToolsForAgentsǁadd_numbers__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_numbers.__signature__ = _mutmut_signature(xǁToolsForAgentsǁadd_numbers__mutmut_orig)
    xǁToolsForAgentsǁadd_numbers__mutmut_orig.__name__ = 'xǁToolsForAgentsǁadd_numbers'
    def xǁToolsForAgentsǁmultiply_numbers__mutmut_orig(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(a, b)
        
    def xǁToolsForAgentsǁmultiply_numbers__mutmut_1(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(None, b)
        
    def xǁToolsForAgentsǁmultiply_numbers__mutmut_2(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(a, None)
        
    def xǁToolsForAgentsǁmultiply_numbers__mutmut_3(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(b)
        
    def xǁToolsForAgentsǁmultiply_numbers__mutmut_4(self, a: int, b: int) -> int:
        """Multiplies two numbers together."""
        return self._instance.multiply_numbers(a, )
        
    
    xǁToolsForAgentsǁmultiply_numbers__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolsForAgentsǁmultiply_numbers__mutmut_1': xǁToolsForAgentsǁmultiply_numbers__mutmut_1, 
        'xǁToolsForAgentsǁmultiply_numbers__mutmut_2': xǁToolsForAgentsǁmultiply_numbers__mutmut_2, 
        'xǁToolsForAgentsǁmultiply_numbers__mutmut_3': xǁToolsForAgentsǁmultiply_numbers__mutmut_3, 
        'xǁToolsForAgentsǁmultiply_numbers__mutmut_4': xǁToolsForAgentsǁmultiply_numbers__mutmut_4
    }
    
    def multiply_numbers(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolsForAgentsǁmultiply_numbers__mutmut_orig"), object.__getattribute__(self, "xǁToolsForAgentsǁmultiply_numbers__mutmut_mutants"), args, kwargs, self)
        return result 
    
    multiply_numbers.__signature__ = _mutmut_signature(xǁToolsForAgentsǁmultiply_numbers__mutmut_orig)
    xǁToolsForAgentsǁmultiply_numbers__mutmut_orig.__name__ = 'xǁToolsForAgentsǁmultiply_numbers'
    def xǁToolsForAgentsǁget_weather__mutmut_orig(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        return self._instance.get_weather(city)
    def xǁToolsForAgentsǁget_weather__mutmut_1(self, city: str) -> str:
        """Gets weather for a city using API key if provided."""
        return self._instance.get_weather(None)
    
    xǁToolsForAgentsǁget_weather__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolsForAgentsǁget_weather__mutmut_1': xǁToolsForAgentsǁget_weather__mutmut_1
    }
    
    def get_weather(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolsForAgentsǁget_weather__mutmut_orig"), object.__getattribute__(self, "xǁToolsForAgentsǁget_weather__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_weather.__signature__ = _mutmut_signature(xǁToolsForAgentsǁget_weather__mutmut_orig)
    xǁToolsForAgentsǁget_weather__mutmut_orig.__name__ = 'xǁToolsForAgentsǁget_weather'
    
    def xǁToolsForAgentsǁget_user_data__mutmut_orig(self, user_id: str) -> Dict:
        """
        Retrieves user data for a specific user ID.
        This tool returns information the LLM couldn't possibly know.
        """
        return self._instance.get_user_data(user_id)
            
    
    def xǁToolsForAgentsǁget_user_data__mutmut_1(self, user_id: str) -> Dict:
        """
        Retrieves user data for a specific user ID.
        This tool returns information the LLM couldn't possibly know.
        """
        return self._instance.get_user_data(None)
            
    
    xǁToolsForAgentsǁget_user_data__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁToolsForAgentsǁget_user_data__mutmut_1': xǁToolsForAgentsǁget_user_data__mutmut_1
    }
    
    def get_user_data(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁToolsForAgentsǁget_user_data__mutmut_orig"), object.__getattribute__(self, "xǁToolsForAgentsǁget_user_data__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_user_data.__signature__ = _mutmut_signature(xǁToolsForAgentsǁget_user_data__mutmut_orig)
    xǁToolsForAgentsǁget_user_data__mutmut_orig.__name__ = 'xǁToolsForAgentsǁget_user_data'
    def get_call_count(self) -> int:
        """Returns the number of times a tool was called."""
        return self._instance.get_call_count()

class BaseTool:
    """Base class for all tools."""
    
    def xǁBaseToolǁ__init____mutmut_orig(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_1(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = None
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_2(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = None
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_3(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name and func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_4(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = None
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_5(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ and f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_6(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description and func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_7(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = None
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_8(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(None)
        self.schema = self._create_schema()
        
    
    def xǁBaseToolǁ__init____mutmut_9(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool.
        
        Args:
            func: The function to use as a tool
            name: Optional name for the tool (defaults to function name)
            description: Optional description (defaults to function docstring)
        """
        self.func = func
        self.name = name or func.__name__
        self.raw_description = description or func.__doc__ or f"Execute {self.name}"
        self.description = self._clean_docstring(self.raw_description)
        self.schema = None
        
    
    xǁBaseToolǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁ__init____mutmut_1': xǁBaseToolǁ__init____mutmut_1, 
        'xǁBaseToolǁ__init____mutmut_2': xǁBaseToolǁ__init____mutmut_2, 
        'xǁBaseToolǁ__init____mutmut_3': xǁBaseToolǁ__init____mutmut_3, 
        'xǁBaseToolǁ__init____mutmut_4': xǁBaseToolǁ__init____mutmut_4, 
        'xǁBaseToolǁ__init____mutmut_5': xǁBaseToolǁ__init____mutmut_5, 
        'xǁBaseToolǁ__init____mutmut_6': xǁBaseToolǁ__init____mutmut_6, 
        'xǁBaseToolǁ__init____mutmut_7': xǁBaseToolǁ__init____mutmut_7, 
        'xǁBaseToolǁ__init____mutmut_8': xǁBaseToolǁ__init____mutmut_8, 
        'xǁBaseToolǁ__init____mutmut_9': xǁBaseToolǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBaseToolǁ__init____mutmut_orig)
    xǁBaseToolǁ__init____mutmut_orig.__name__ = 'xǁBaseToolǁ__init__'
    def xǁBaseToolǁ_clean_docstring__mutmut_orig(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_1(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_2(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = None
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_3(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split(None)
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_4(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('XX\nXX')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_5(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines or not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_6(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_7(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[1].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_8(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(None)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_9(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(1)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_10(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines or not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_11(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_12(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[+1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_13(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-2].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_14(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_15(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = None
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_16(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 1
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_17(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = None
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_18(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) + len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_19(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                return
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_20(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = None
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_21(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent or line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_22(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) >= indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_23(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(None)
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_24(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(None)
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_25(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.rstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_26(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append(None)  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_27(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("XXXX")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_28(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = None
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_29(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(None)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_30(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = 'XX\nXX'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_31(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result and "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_32(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result and "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_33(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "XXArgs:XX" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_34(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_35(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "ARGS:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_36(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" not in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_37(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "XXParameters:XX" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_38(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_39(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "PARAMETERS:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_40(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" not in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_41(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "XXReturns:XX" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_42(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_43(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "RETURNS:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_44(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" not in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_45(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = None
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_46(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find(None)
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_47(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.rfind("\n\n")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_48(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("XX\n\nXX")
            if first_para_end > 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_49(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end >= 0:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_50(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 1:
                result = result[:first_para_end]
        
        return result.strip()
        
    def xǁBaseToolǁ_clean_docstring__mutmut_51(self, docstring: str) -> str:
        """
        Clean and format a docstring for use in tool definitions.
        
        This removes excessive whitespace, normalizes indentation, and
        formats the docstring to be more readable when sent to LLMs.
        """
        if not docstring:
            return f"Execute {self.name}"
        
        # Split by lines and remove empty lines at start/end
        lines = docstring.split('\n')
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        if not lines:
            return f"Execute {self.name}"
        
        # Determine the indentation level (from the first non-empty line)
        indent = 0
        for line in lines:
            if line.strip():
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                break
        
        # Remove common indentation from all lines
        cleaned_lines = []
        for line in lines:
            if line.strip():  # If line is not empty
                # Remove only up to 'indent' spaces to preserve nested indentation
                if len(line) > indent and line[:indent].isspace():
                    cleaned_lines.append(line[indent:])
                else:
                    cleaned_lines.append(line.lstrip())
            else:
                cleaned_lines.append("")  # Keep empty lines for paragraph breaks
                
        # Join lines and cleanup extra whitespace
        result = '\n'.join(cleaned_lines)
        
        # If the result has "Args:" or similar sections, simplify for the main description
        # by taking just the first paragraph
        if "Args:" in result or "Parameters:" in result or "Returns:" in result:
            # Extract just the first paragraph for the description
            first_para_end = result.find("\n\n")
            if first_para_end > 0:
                result = None
        
        return result.strip()
        
    
    xǁBaseToolǁ_clean_docstring__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁ_clean_docstring__mutmut_1': xǁBaseToolǁ_clean_docstring__mutmut_1, 
        'xǁBaseToolǁ_clean_docstring__mutmut_2': xǁBaseToolǁ_clean_docstring__mutmut_2, 
        'xǁBaseToolǁ_clean_docstring__mutmut_3': xǁBaseToolǁ_clean_docstring__mutmut_3, 
        'xǁBaseToolǁ_clean_docstring__mutmut_4': xǁBaseToolǁ_clean_docstring__mutmut_4, 
        'xǁBaseToolǁ_clean_docstring__mutmut_5': xǁBaseToolǁ_clean_docstring__mutmut_5, 
        'xǁBaseToolǁ_clean_docstring__mutmut_6': xǁBaseToolǁ_clean_docstring__mutmut_6, 
        'xǁBaseToolǁ_clean_docstring__mutmut_7': xǁBaseToolǁ_clean_docstring__mutmut_7, 
        'xǁBaseToolǁ_clean_docstring__mutmut_8': xǁBaseToolǁ_clean_docstring__mutmut_8, 
        'xǁBaseToolǁ_clean_docstring__mutmut_9': xǁBaseToolǁ_clean_docstring__mutmut_9, 
        'xǁBaseToolǁ_clean_docstring__mutmut_10': xǁBaseToolǁ_clean_docstring__mutmut_10, 
        'xǁBaseToolǁ_clean_docstring__mutmut_11': xǁBaseToolǁ_clean_docstring__mutmut_11, 
        'xǁBaseToolǁ_clean_docstring__mutmut_12': xǁBaseToolǁ_clean_docstring__mutmut_12, 
        'xǁBaseToolǁ_clean_docstring__mutmut_13': xǁBaseToolǁ_clean_docstring__mutmut_13, 
        'xǁBaseToolǁ_clean_docstring__mutmut_14': xǁBaseToolǁ_clean_docstring__mutmut_14, 
        'xǁBaseToolǁ_clean_docstring__mutmut_15': xǁBaseToolǁ_clean_docstring__mutmut_15, 
        'xǁBaseToolǁ_clean_docstring__mutmut_16': xǁBaseToolǁ_clean_docstring__mutmut_16, 
        'xǁBaseToolǁ_clean_docstring__mutmut_17': xǁBaseToolǁ_clean_docstring__mutmut_17, 
        'xǁBaseToolǁ_clean_docstring__mutmut_18': xǁBaseToolǁ_clean_docstring__mutmut_18, 
        'xǁBaseToolǁ_clean_docstring__mutmut_19': xǁBaseToolǁ_clean_docstring__mutmut_19, 
        'xǁBaseToolǁ_clean_docstring__mutmut_20': xǁBaseToolǁ_clean_docstring__mutmut_20, 
        'xǁBaseToolǁ_clean_docstring__mutmut_21': xǁBaseToolǁ_clean_docstring__mutmut_21, 
        'xǁBaseToolǁ_clean_docstring__mutmut_22': xǁBaseToolǁ_clean_docstring__mutmut_22, 
        'xǁBaseToolǁ_clean_docstring__mutmut_23': xǁBaseToolǁ_clean_docstring__mutmut_23, 
        'xǁBaseToolǁ_clean_docstring__mutmut_24': xǁBaseToolǁ_clean_docstring__mutmut_24, 
        'xǁBaseToolǁ_clean_docstring__mutmut_25': xǁBaseToolǁ_clean_docstring__mutmut_25, 
        'xǁBaseToolǁ_clean_docstring__mutmut_26': xǁBaseToolǁ_clean_docstring__mutmut_26, 
        'xǁBaseToolǁ_clean_docstring__mutmut_27': xǁBaseToolǁ_clean_docstring__mutmut_27, 
        'xǁBaseToolǁ_clean_docstring__mutmut_28': xǁBaseToolǁ_clean_docstring__mutmut_28, 
        'xǁBaseToolǁ_clean_docstring__mutmut_29': xǁBaseToolǁ_clean_docstring__mutmut_29, 
        'xǁBaseToolǁ_clean_docstring__mutmut_30': xǁBaseToolǁ_clean_docstring__mutmut_30, 
        'xǁBaseToolǁ_clean_docstring__mutmut_31': xǁBaseToolǁ_clean_docstring__mutmut_31, 
        'xǁBaseToolǁ_clean_docstring__mutmut_32': xǁBaseToolǁ_clean_docstring__mutmut_32, 
        'xǁBaseToolǁ_clean_docstring__mutmut_33': xǁBaseToolǁ_clean_docstring__mutmut_33, 
        'xǁBaseToolǁ_clean_docstring__mutmut_34': xǁBaseToolǁ_clean_docstring__mutmut_34, 
        'xǁBaseToolǁ_clean_docstring__mutmut_35': xǁBaseToolǁ_clean_docstring__mutmut_35, 
        'xǁBaseToolǁ_clean_docstring__mutmut_36': xǁBaseToolǁ_clean_docstring__mutmut_36, 
        'xǁBaseToolǁ_clean_docstring__mutmut_37': xǁBaseToolǁ_clean_docstring__mutmut_37, 
        'xǁBaseToolǁ_clean_docstring__mutmut_38': xǁBaseToolǁ_clean_docstring__mutmut_38, 
        'xǁBaseToolǁ_clean_docstring__mutmut_39': xǁBaseToolǁ_clean_docstring__mutmut_39, 
        'xǁBaseToolǁ_clean_docstring__mutmut_40': xǁBaseToolǁ_clean_docstring__mutmut_40, 
        'xǁBaseToolǁ_clean_docstring__mutmut_41': xǁBaseToolǁ_clean_docstring__mutmut_41, 
        'xǁBaseToolǁ_clean_docstring__mutmut_42': xǁBaseToolǁ_clean_docstring__mutmut_42, 
        'xǁBaseToolǁ_clean_docstring__mutmut_43': xǁBaseToolǁ_clean_docstring__mutmut_43, 
        'xǁBaseToolǁ_clean_docstring__mutmut_44': xǁBaseToolǁ_clean_docstring__mutmut_44, 
        'xǁBaseToolǁ_clean_docstring__mutmut_45': xǁBaseToolǁ_clean_docstring__mutmut_45, 
        'xǁBaseToolǁ_clean_docstring__mutmut_46': xǁBaseToolǁ_clean_docstring__mutmut_46, 
        'xǁBaseToolǁ_clean_docstring__mutmut_47': xǁBaseToolǁ_clean_docstring__mutmut_47, 
        'xǁBaseToolǁ_clean_docstring__mutmut_48': xǁBaseToolǁ_clean_docstring__mutmut_48, 
        'xǁBaseToolǁ_clean_docstring__mutmut_49': xǁBaseToolǁ_clean_docstring__mutmut_49, 
        'xǁBaseToolǁ_clean_docstring__mutmut_50': xǁBaseToolǁ_clean_docstring__mutmut_50, 
        'xǁBaseToolǁ_clean_docstring__mutmut_51': xǁBaseToolǁ_clean_docstring__mutmut_51
    }
    
    def _clean_docstring(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁ_clean_docstring__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁ_clean_docstring__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _clean_docstring.__signature__ = _mutmut_signature(xǁBaseToolǁ_clean_docstring__mutmut_orig)
    xǁBaseToolǁ_clean_docstring__mutmut_orig.__name__ = 'xǁBaseToolǁ_clean_docstring'
    def xǁBaseToolǁ_create_schema__mutmut_orig(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_1(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = None
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_2(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(None)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_3(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = None
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_4(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(None)
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_5(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = None
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_6(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(None, **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_7(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(**fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_8(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", )
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_9(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name - "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_10(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "XXSchemaXX", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_11(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_12(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "SCHEMA", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = self.raw_description
        return ToolSchema
    def xǁBaseToolǁ_create_schema__mutmut_13(self) -> Type[BaseModel]:
        """Create a Pydantic model from the function signature."""
        sig = inspect.signature(self.func)
        fields = self._get_schema_fields(sig)
        ToolSchema = create_model(self.name + "Schema", **fields)
        
        # Add docstring to the schema
        ToolSchema.__doc__ = None
        return ToolSchema
    
    xǁBaseToolǁ_create_schema__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁ_create_schema__mutmut_1': xǁBaseToolǁ_create_schema__mutmut_1, 
        'xǁBaseToolǁ_create_schema__mutmut_2': xǁBaseToolǁ_create_schema__mutmut_2, 
        'xǁBaseToolǁ_create_schema__mutmut_3': xǁBaseToolǁ_create_schema__mutmut_3, 
        'xǁBaseToolǁ_create_schema__mutmut_4': xǁBaseToolǁ_create_schema__mutmut_4, 
        'xǁBaseToolǁ_create_schema__mutmut_5': xǁBaseToolǁ_create_schema__mutmut_5, 
        'xǁBaseToolǁ_create_schema__mutmut_6': xǁBaseToolǁ_create_schema__mutmut_6, 
        'xǁBaseToolǁ_create_schema__mutmut_7': xǁBaseToolǁ_create_schema__mutmut_7, 
        'xǁBaseToolǁ_create_schema__mutmut_8': xǁBaseToolǁ_create_schema__mutmut_8, 
        'xǁBaseToolǁ_create_schema__mutmut_9': xǁBaseToolǁ_create_schema__mutmut_9, 
        'xǁBaseToolǁ_create_schema__mutmut_10': xǁBaseToolǁ_create_schema__mutmut_10, 
        'xǁBaseToolǁ_create_schema__mutmut_11': xǁBaseToolǁ_create_schema__mutmut_11, 
        'xǁBaseToolǁ_create_schema__mutmut_12': xǁBaseToolǁ_create_schema__mutmut_12, 
        'xǁBaseToolǁ_create_schema__mutmut_13': xǁBaseToolǁ_create_schema__mutmut_13
    }
    
    def _create_schema(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁ_create_schema__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁ_create_schema__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _create_schema.__signature__ = _mutmut_signature(xǁBaseToolǁ_create_schema__mutmut_orig)
    xǁBaseToolǁ_create_schema__mutmut_orig.__name__ = 'xǁBaseToolǁ_create_schema'
    
    def xǁBaseToolǁ_get_schema_fields__mutmut_orig(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = {}
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁBaseToolǁ_get_schema_fields__mutmut_1(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = None
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁBaseToolǁ_get_schema_fields__mutmut_2(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = {}
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is not inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁBaseToolǁ_get_schema_fields__mutmut_3(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = {}
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = None
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁBaseToolǁ_get_schema_fields__mutmut_4(self, sig: inspect.Signature) -> Dict:
        """Extract fields from function signature for schema creation."""
        fields = {}
        for name, param in sig.parameters.items():
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = None
        return fields
    
    xǁBaseToolǁ_get_schema_fields__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁ_get_schema_fields__mutmut_1': xǁBaseToolǁ_get_schema_fields__mutmut_1, 
        'xǁBaseToolǁ_get_schema_fields__mutmut_2': xǁBaseToolǁ_get_schema_fields__mutmut_2, 
        'xǁBaseToolǁ_get_schema_fields__mutmut_3': xǁBaseToolǁ_get_schema_fields__mutmut_3, 
        'xǁBaseToolǁ_get_schema_fields__mutmut_4': xǁBaseToolǁ_get_schema_fields__mutmut_4
    }
    
    def _get_schema_fields(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁ_get_schema_fields__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁ_get_schema_fields__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_schema_fields.__signature__ = _mutmut_signature(xǁBaseToolǁ_get_schema_fields__mutmut_orig)
    xǁBaseToolǁ_get_schema_fields__mutmut_orig.__name__ = 'xǁBaseToolǁ_get_schema_fields'
    
    def xǁBaseToolǁexecute__mutmut_orig(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        # Execute the function with validated arguments
        return self.func(**validated_args.model_dump())
    
    def xǁBaseToolǁexecute__mutmut_1(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = None
        # Execute the function with validated arguments
        return self.func(**validated_args.model_dump())
    
    xǁBaseToolǁexecute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁexecute__mutmut_1': xǁBaseToolǁexecute__mutmut_1
    }
    
    def execute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁexecute__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁexecute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute.__signature__ = _mutmut_signature(xǁBaseToolǁexecute__mutmut_orig)
    xǁBaseToolǁexecute__mutmut_orig.__name__ = 'xǁBaseToolǁexecute'
    
    def xǁBaseToolǁto_function_definition__mutmut_orig(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_1(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = None
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_2(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'XXdescriptionXX' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_3(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'DESCRIPTION' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_4(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' not in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_5(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "XXnameXX": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_6(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "NAME": self.name,
            "description": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_7(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "XXdescriptionXX": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_8(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "DESCRIPTION": self.description,
            "parameters": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_9(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "XXparametersXX": schema_dict
        }
        
    
    def xǁBaseToolǁto_function_definition__mutmut_10(self) -> Dict:
        """Convert tool to function definition compatible with LLM APIs."""
        schema_dict = self.schema.model_json_schema()
        
        # Replace schema description with our cleaned description to avoid duplication
        if 'description' in schema_dict:
            # Use a concise version in the parameters section
            pass  # Keep the schema description for parameter details
        
        return {
            "name": self.name,
            "description": self.description,
            "PARAMETERS": schema_dict
        }
        
    
    xǁBaseToolǁto_function_definition__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBaseToolǁto_function_definition__mutmut_1': xǁBaseToolǁto_function_definition__mutmut_1, 
        'xǁBaseToolǁto_function_definition__mutmut_2': xǁBaseToolǁto_function_definition__mutmut_2, 
        'xǁBaseToolǁto_function_definition__mutmut_3': xǁBaseToolǁto_function_definition__mutmut_3, 
        'xǁBaseToolǁto_function_definition__mutmut_4': xǁBaseToolǁto_function_definition__mutmut_4, 
        'xǁBaseToolǁto_function_definition__mutmut_5': xǁBaseToolǁto_function_definition__mutmut_5, 
        'xǁBaseToolǁto_function_definition__mutmut_6': xǁBaseToolǁto_function_definition__mutmut_6, 
        'xǁBaseToolǁto_function_definition__mutmut_7': xǁBaseToolǁto_function_definition__mutmut_7, 
        'xǁBaseToolǁto_function_definition__mutmut_8': xǁBaseToolǁto_function_definition__mutmut_8, 
        'xǁBaseToolǁto_function_definition__mutmut_9': xǁBaseToolǁto_function_definition__mutmut_9, 
        'xǁBaseToolǁto_function_definition__mutmut_10': xǁBaseToolǁto_function_definition__mutmut_10
    }
    
    def to_function_definition(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBaseToolǁto_function_definition__mutmut_orig"), object.__getattribute__(self, "xǁBaseToolǁto_function_definition__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_function_definition.__signature__ = _mutmut_signature(xǁBaseToolǁto_function_definition__mutmut_orig)
    xǁBaseToolǁto_function_definition__mutmut_orig.__name__ = 'xǁBaseToolǁto_function_definition'
    def to_dict(self) -> Dict:
        """Alias for to_function_definition for compatibility with new tool calling system."""
        return self.to_function_definition()


class FunctionTool(BaseTool):
    """Tool implementation for standalone functions."""
    
    def xǁFunctionToolǁ__init____mutmut_orig(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, name, description)
    
    def xǁFunctionToolǁ__init____mutmut_1(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(None, name, description)
    
    def xǁFunctionToolǁ__init____mutmut_2(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, None, description)
    
    def xǁFunctionToolǁ__init____mutmut_3(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, name, None)
    
    def xǁFunctionToolǁ__init____mutmut_4(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(name, description)
    
    def xǁFunctionToolǁ__init____mutmut_5(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, description)
    
    def xǁFunctionToolǁ__init____mutmut_6(self, func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(func, name, )
    
    xǁFunctionToolǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFunctionToolǁ__init____mutmut_1': xǁFunctionToolǁ__init____mutmut_1, 
        'xǁFunctionToolǁ__init____mutmut_2': xǁFunctionToolǁ__init____mutmut_2, 
        'xǁFunctionToolǁ__init____mutmut_3': xǁFunctionToolǁ__init____mutmut_3, 
        'xǁFunctionToolǁ__init____mutmut_4': xǁFunctionToolǁ__init____mutmut_4, 
        'xǁFunctionToolǁ__init____mutmut_5': xǁFunctionToolǁ__init____mutmut_5, 
        'xǁFunctionToolǁ__init____mutmut_6': xǁFunctionToolǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFunctionToolǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFunctionToolǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFunctionToolǁ__init____mutmut_orig)
    xǁFunctionToolǁ__init____mutmut_orig.__name__ = 'xǁFunctionToolǁ__init__'


class InstanceMethodTool(BaseTool):
    """Tool implementation for instance methods."""
    
    def xǁInstanceMethodToolǁ__init____mutmut_orig(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_1(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = None
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_2(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = None
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_3(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') or method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_4(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(None, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_5(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, None) and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_6(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr('__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_7(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, ) and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_8(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, 'XX__self__XX') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_9(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__SELF__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_10(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is not instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_11(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = None
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_12(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(None, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_13(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, None)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_14(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_15(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, )
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_16(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = None
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_17(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(None, name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_18(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, None, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_19(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, None)
    
    def xǁInstanceMethodToolǁ__init____mutmut_20(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(name or method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_21(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_22(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, )
    
    def xǁInstanceMethodToolǁ__init____mutmut_23(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name and method.__name__, description or method.__doc__)
    
    def xǁInstanceMethodToolǁ__init____mutmut_24(self, method: Callable, instance: Any, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a tool from an instance method.
        
        Args:
            method: The instance method to use as a tool
            instance: The instance the method belongs to
            name: Optional name for the tool (defaults to method name)
            description: Optional description (defaults to method docstring)
        """
        self.instance = instance
        
        # Check if this is a class method or static method
        if isinstance(instance, type):
            # This is a class method or static method
            self.unbound_method = method
            
            # Create a wrapper function that handles the class correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return method(**kwargs)
        else:
            # This is an instance method
            # Get the unbound method from the class
            if hasattr(method, '__self__') and method.__self__ is instance:
                # This is a bound method, get the unbound version
                self.unbound_method = getattr(method.__self__.__class__, method.__name__)
            else:
                # Already unbound or not a method
                self.unbound_method = method
                
            # Create a wrapper function that handles the instance correctly
            @functools.wraps(method)
            def wrapper(**kwargs):
                return self.unbound_method(instance, **kwargs)
        
        super().__init__(wrapper, name or method.__name__, description and method.__doc__)
    
    xǁInstanceMethodToolǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInstanceMethodToolǁ__init____mutmut_1': xǁInstanceMethodToolǁ__init____mutmut_1, 
        'xǁInstanceMethodToolǁ__init____mutmut_2': xǁInstanceMethodToolǁ__init____mutmut_2, 
        'xǁInstanceMethodToolǁ__init____mutmut_3': xǁInstanceMethodToolǁ__init____mutmut_3, 
        'xǁInstanceMethodToolǁ__init____mutmut_4': xǁInstanceMethodToolǁ__init____mutmut_4, 
        'xǁInstanceMethodToolǁ__init____mutmut_5': xǁInstanceMethodToolǁ__init____mutmut_5, 
        'xǁInstanceMethodToolǁ__init____mutmut_6': xǁInstanceMethodToolǁ__init____mutmut_6, 
        'xǁInstanceMethodToolǁ__init____mutmut_7': xǁInstanceMethodToolǁ__init____mutmut_7, 
        'xǁInstanceMethodToolǁ__init____mutmut_8': xǁInstanceMethodToolǁ__init____mutmut_8, 
        'xǁInstanceMethodToolǁ__init____mutmut_9': xǁInstanceMethodToolǁ__init____mutmut_9, 
        'xǁInstanceMethodToolǁ__init____mutmut_10': xǁInstanceMethodToolǁ__init____mutmut_10, 
        'xǁInstanceMethodToolǁ__init____mutmut_11': xǁInstanceMethodToolǁ__init____mutmut_11, 
        'xǁInstanceMethodToolǁ__init____mutmut_12': xǁInstanceMethodToolǁ__init____mutmut_12, 
        'xǁInstanceMethodToolǁ__init____mutmut_13': xǁInstanceMethodToolǁ__init____mutmut_13, 
        'xǁInstanceMethodToolǁ__init____mutmut_14': xǁInstanceMethodToolǁ__init____mutmut_14, 
        'xǁInstanceMethodToolǁ__init____mutmut_15': xǁInstanceMethodToolǁ__init____mutmut_15, 
        'xǁInstanceMethodToolǁ__init____mutmut_16': xǁInstanceMethodToolǁ__init____mutmut_16, 
        'xǁInstanceMethodToolǁ__init____mutmut_17': xǁInstanceMethodToolǁ__init____mutmut_17, 
        'xǁInstanceMethodToolǁ__init____mutmut_18': xǁInstanceMethodToolǁ__init____mutmut_18, 
        'xǁInstanceMethodToolǁ__init____mutmut_19': xǁInstanceMethodToolǁ__init____mutmut_19, 
        'xǁInstanceMethodToolǁ__init____mutmut_20': xǁInstanceMethodToolǁ__init____mutmut_20, 
        'xǁInstanceMethodToolǁ__init____mutmut_21': xǁInstanceMethodToolǁ__init____mutmut_21, 
        'xǁInstanceMethodToolǁ__init____mutmut_22': xǁInstanceMethodToolǁ__init____mutmut_22, 
        'xǁInstanceMethodToolǁ__init____mutmut_23': xǁInstanceMethodToolǁ__init____mutmut_23, 
        'xǁInstanceMethodToolǁ__init____mutmut_24': xǁInstanceMethodToolǁ__init____mutmut_24
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInstanceMethodToolǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁInstanceMethodToolǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁInstanceMethodToolǁ__init____mutmut_orig)
    xǁInstanceMethodToolǁ__init____mutmut_orig.__name__ = 'xǁInstanceMethodToolǁ__init__'
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_orig(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_1(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = None
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_2(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(None)
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_3(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params or params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_4(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[1][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_5(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][1] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_6(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] != 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_7(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'XXselfXX':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_8(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'SELF':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_9(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = None
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_10(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[2:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_11(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = None
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_12(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is not inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_13(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = None
            else:
                fields[name] = (param.annotation, ...)
        return fields
    
    def xǁInstanceMethodToolǁ_get_schema_fields__mutmut_14(self, sig: inspect.Signature) -> Dict:
        """Extract fields from method signature, excluding 'self'."""
        params = list(sig.parameters.items())
        # Skip 'self' parameter if present
        if params and params[0][0] == 'self':
            params = params[1:]
        
        fields = {}
        for name, param in params:
            # Handle parameters without type annotations (inspect._empty)
            if param.annotation is inspect._empty:
                fields[name] = (Any, ...)
            else:
                fields[name] = None
        return fields
    
    xǁInstanceMethodToolǁ_get_schema_fields__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_1': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_1, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_2': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_2, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_3': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_3, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_4': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_4, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_5': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_5, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_6': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_6, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_7': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_7, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_8': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_8, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_9': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_9, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_10': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_10, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_11': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_11, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_12': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_12, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_13': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_13, 
        'xǁInstanceMethodToolǁ_get_schema_fields__mutmut_14': xǁInstanceMethodToolǁ_get_schema_fields__mutmut_14
    }
    
    def _get_schema_fields(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInstanceMethodToolǁ_get_schema_fields__mutmut_orig"), object.__getattribute__(self, "xǁInstanceMethodToolǁ_get_schema_fields__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _get_schema_fields.__signature__ = _mutmut_signature(xǁInstanceMethodToolǁ_get_schema_fields__mutmut_orig)
    xǁInstanceMethodToolǁ_get_schema_fields__mutmut_orig.__name__ = 'xǁInstanceMethodToolǁ_get_schema_fields'
    
    def xǁInstanceMethodToolǁexecute__mutmut_orig(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = self.schema(**kwargs)
        
        # The wrapper function created in __init__ already handles the instance correctly
        return self.func(**validated_args.model_dump())
    
    def xǁInstanceMethodToolǁexecute__mutmut_1(self, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        # Validate arguments using the schema
        validated_args = None
        
        # The wrapper function created in __init__ already handles the instance correctly
        return self.func(**validated_args.model_dump())
    
    xǁInstanceMethodToolǁexecute__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁInstanceMethodToolǁexecute__mutmut_1': xǁInstanceMethodToolǁexecute__mutmut_1
    }
    
    def execute(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁInstanceMethodToolǁexecute__mutmut_orig"), object.__getattribute__(self, "xǁInstanceMethodToolǁexecute__mutmut_mutants"), args, kwargs, self)
        return result 
    
    execute.__signature__ = _mutmut_signature(xǁInstanceMethodToolǁexecute__mutmut_orig)
    xǁInstanceMethodToolǁexecute__mutmut_orig.__name__ = 'xǁInstanceMethodToolǁexecute'


class StaticMethodTool(BaseTool):
    """Tool implementation for static methods."""
    
    def xǁStaticMethodToolǁ__init____mutmut_orig(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, name, description)
    
    def xǁStaticMethodToolǁ__init____mutmut_1(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(None, name, description)
    
    def xǁStaticMethodToolǁ__init____mutmut_2(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, None, description)
    
    def xǁStaticMethodToolǁ__init____mutmut_3(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, name, None)
    
    def xǁStaticMethodToolǁ__init____mutmut_4(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(name, description)
    
    def xǁStaticMethodToolǁ__init____mutmut_5(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, description)
    
    def xǁStaticMethodToolǁ__init____mutmut_6(self, method: Callable, name: Optional[str] = None, description: Optional[str] = None):
        super().__init__(method, name, )
    
    xǁStaticMethodToolǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStaticMethodToolǁ__init____mutmut_1': xǁStaticMethodToolǁ__init____mutmut_1, 
        'xǁStaticMethodToolǁ__init____mutmut_2': xǁStaticMethodToolǁ__init____mutmut_2, 
        'xǁStaticMethodToolǁ__init____mutmut_3': xǁStaticMethodToolǁ__init____mutmut_3, 
        'xǁStaticMethodToolǁ__init____mutmut_4': xǁStaticMethodToolǁ__init____mutmut_4, 
        'xǁStaticMethodToolǁ__init____mutmut_5': xǁStaticMethodToolǁ__init____mutmut_5, 
        'xǁStaticMethodToolǁ__init____mutmut_6': xǁStaticMethodToolǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStaticMethodToolǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStaticMethodToolǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStaticMethodToolǁ__init____mutmut_orig)
    xǁStaticMethodToolǁ__init____mutmut_orig.__name__ = 'xǁStaticMethodToolǁ__init__'


def x_get_function_definitions__mutmut_orig(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_1(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = None
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_2(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(None)
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_3(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(None):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_4(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = None
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_5(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(None)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_6(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(None)
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_7(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) or "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_8(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "XXnameXX" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_9(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "NAME" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_10(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" not in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_11(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(None)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_12(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = None
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_13(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["XXschemaXX"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_14(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["SCHEMA"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_15(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append(None)
            
    return function_definitions


def x_get_function_definitions__mutmut_16(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "XXnameXX": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_17(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "NAME": tool_name,
                "description": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_18(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "XXdescriptionXX": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_19(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "DESCRIPTION": schema.__doc__,
                "parameters": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_20(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "XXparametersXX": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions


def x_get_function_definitions__mutmut_21(tool_functions=None):
    """
    Convert tools to function definitions compatible with LLM APIs.
    
    Args:
        tool_functions: Optional list of tool functions to convert. If None, uses all registered tools.
    
    Returns:
        list: List of function definitions in the format expected by OpenAI-compatible APIs
    """
    function_definitions = []
    
    # If specific tools are provided, convert them
    if tool_functions:
        for tool in tool_functions:
            if isinstance(tool, BaseTool):
                # For BaseTool instances, use their to_dict method
                function_definitions.append(tool.to_dict())
            elif callable(tool):
                # For functions, create a temporary FunctionTool and get its definition
                temp_tool = FunctionTool(tool)
                function_definitions.append(temp_tool.to_dict())
            elif isinstance(tool, dict) and "name" in tool:
                # For dictionaries that already look like function definitions
                function_definitions.append(tool)
    else:
        # Otherwise, use all registered tools
        for tool_name, tool_data in TOOLS.items():
            schema = tool_data["schema"]
            function_definitions.append({
                "name": tool_name,
                "description": schema.__doc__,
                "PARAMETERS": schema.schema()  # Convert Pydantic model to JSON schema
            })
            
    return function_definitions

x_get_function_definitions__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_function_definitions__mutmut_1': x_get_function_definitions__mutmut_1, 
    'x_get_function_definitions__mutmut_2': x_get_function_definitions__mutmut_2, 
    'x_get_function_definitions__mutmut_3': x_get_function_definitions__mutmut_3, 
    'x_get_function_definitions__mutmut_4': x_get_function_definitions__mutmut_4, 
    'x_get_function_definitions__mutmut_5': x_get_function_definitions__mutmut_5, 
    'x_get_function_definitions__mutmut_6': x_get_function_definitions__mutmut_6, 
    'x_get_function_definitions__mutmut_7': x_get_function_definitions__mutmut_7, 
    'x_get_function_definitions__mutmut_8': x_get_function_definitions__mutmut_8, 
    'x_get_function_definitions__mutmut_9': x_get_function_definitions__mutmut_9, 
    'x_get_function_definitions__mutmut_10': x_get_function_definitions__mutmut_10, 
    'x_get_function_definitions__mutmut_11': x_get_function_definitions__mutmut_11, 
    'x_get_function_definitions__mutmut_12': x_get_function_definitions__mutmut_12, 
    'x_get_function_definitions__mutmut_13': x_get_function_definitions__mutmut_13, 
    'x_get_function_definitions__mutmut_14': x_get_function_definitions__mutmut_14, 
    'x_get_function_definitions__mutmut_15': x_get_function_definitions__mutmut_15, 
    'x_get_function_definitions__mutmut_16': x_get_function_definitions__mutmut_16, 
    'x_get_function_definitions__mutmut_17': x_get_function_definitions__mutmut_17, 
    'x_get_function_definitions__mutmut_18': x_get_function_definitions__mutmut_18, 
    'x_get_function_definitions__mutmut_19': x_get_function_definitions__mutmut_19, 
    'x_get_function_definitions__mutmut_20': x_get_function_definitions__mutmut_20, 
    'x_get_function_definitions__mutmut_21': x_get_function_definitions__mutmut_21
}

def get_function_definitions(*args, **kwargs):
    result = _mutmut_trampoline(x_get_function_definitions__mutmut_orig, x_get_function_definitions__mutmut_mutants, args, kwargs)
    return result 

get_function_definitions.__signature__ = _mutmut_signature(x_get_function_definitions__mutmut_orig)
x_get_function_definitions__mutmut_orig.__name__ = 'x_get_function_definitions'


def x_liteagent_tool__mutmut_orig(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_1(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(None):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_2(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_3(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = None
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_4(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(None, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_5(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, None, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_6(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, None, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_7(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, None)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_8(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_9(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_10(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_11(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, )
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_12(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = None
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_13(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(None, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_14(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, None, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_15(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, None)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_16(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_17(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_18(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, )
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_19(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') or '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_20(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) or hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_21(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(None) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_22(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(None, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_23(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, None) and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_24(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr('__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_25(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, ) and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_26(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, 'XX__qualname__XX') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_27(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__QUALNAME__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_28(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and 'XX.XX' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_29(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' not in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_30(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = None
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_31(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(None, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_32(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, None, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_33(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, None)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_34(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_35(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_36(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, )
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_37(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'XXtool_instanceXX' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_38(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'TOOL_INSTANCE' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_39(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' not in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_40(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = None
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_41(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "XXschemaXX": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_42(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "SCHEMA": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_43(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "XXfunctionXX": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_44(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "FUNCTION": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_45(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is not None:
        return decorator
    return decorator(func)


def x_liteagent_tool__mutmut_46(func=None, *, name=None, description=None):
    """
    Universal decorator to register any function or method as a tool.
    Automatically detects the function type and creates the appropriate tool instance.
    
    This is the preferred way to register tools in LiteAgent.
    
    Args:
        func: The function or method to register
        name: Optional custom name for the tool
        description: Optional custom description
        
    Returns:
        Decorator function or decorated function
    """
    def decorator(f):
        # Determine the appropriate tool type
        if inspect.ismethod(f):
            # For bound methods
            if f.__self__ is not None:
                tool_instance = InstanceMethodTool(f, f.__self__, name, description)
            else:
                # For static/class methods
                tool_instance = StaticMethodTool(f, name, description)
        elif inspect.isfunction(f) and hasattr(f, '__qualname__') and '.' in f.__qualname__:
            # This might be a class method or static method that's not bound yet
            # We'll handle it when it's actually used in the agent
            pass
        else:
            # For regular functions
            tool_instance = FunctionTool(f, name, description)
        
        # Register the tool
        if 'tool_instance' in locals():
            TOOLS[tool_instance.name] = {
                "schema": tool_instance.schema,
                "function": tool_instance.func
            }
        
        return f
    
    # Handle both @liteagent_tool and @liteagent_tool(name="custom")
    if func is None:
        return decorator
    return decorator(None)

x_liteagent_tool__mutmut_mutants : ClassVar[MutantDict] = {
'x_liteagent_tool__mutmut_1': x_liteagent_tool__mutmut_1, 
    'x_liteagent_tool__mutmut_2': x_liteagent_tool__mutmut_2, 
    'x_liteagent_tool__mutmut_3': x_liteagent_tool__mutmut_3, 
    'x_liteagent_tool__mutmut_4': x_liteagent_tool__mutmut_4, 
    'x_liteagent_tool__mutmut_5': x_liteagent_tool__mutmut_5, 
    'x_liteagent_tool__mutmut_6': x_liteagent_tool__mutmut_6, 
    'x_liteagent_tool__mutmut_7': x_liteagent_tool__mutmut_7, 
    'x_liteagent_tool__mutmut_8': x_liteagent_tool__mutmut_8, 
    'x_liteagent_tool__mutmut_9': x_liteagent_tool__mutmut_9, 
    'x_liteagent_tool__mutmut_10': x_liteagent_tool__mutmut_10, 
    'x_liteagent_tool__mutmut_11': x_liteagent_tool__mutmut_11, 
    'x_liteagent_tool__mutmut_12': x_liteagent_tool__mutmut_12, 
    'x_liteagent_tool__mutmut_13': x_liteagent_tool__mutmut_13, 
    'x_liteagent_tool__mutmut_14': x_liteagent_tool__mutmut_14, 
    'x_liteagent_tool__mutmut_15': x_liteagent_tool__mutmut_15, 
    'x_liteagent_tool__mutmut_16': x_liteagent_tool__mutmut_16, 
    'x_liteagent_tool__mutmut_17': x_liteagent_tool__mutmut_17, 
    'x_liteagent_tool__mutmut_18': x_liteagent_tool__mutmut_18, 
    'x_liteagent_tool__mutmut_19': x_liteagent_tool__mutmut_19, 
    'x_liteagent_tool__mutmut_20': x_liteagent_tool__mutmut_20, 
    'x_liteagent_tool__mutmut_21': x_liteagent_tool__mutmut_21, 
    'x_liteagent_tool__mutmut_22': x_liteagent_tool__mutmut_22, 
    'x_liteagent_tool__mutmut_23': x_liteagent_tool__mutmut_23, 
    'x_liteagent_tool__mutmut_24': x_liteagent_tool__mutmut_24, 
    'x_liteagent_tool__mutmut_25': x_liteagent_tool__mutmut_25, 
    'x_liteagent_tool__mutmut_26': x_liteagent_tool__mutmut_26, 
    'x_liteagent_tool__mutmut_27': x_liteagent_tool__mutmut_27, 
    'x_liteagent_tool__mutmut_28': x_liteagent_tool__mutmut_28, 
    'x_liteagent_tool__mutmut_29': x_liteagent_tool__mutmut_29, 
    'x_liteagent_tool__mutmut_30': x_liteagent_tool__mutmut_30, 
    'x_liteagent_tool__mutmut_31': x_liteagent_tool__mutmut_31, 
    'x_liteagent_tool__mutmut_32': x_liteagent_tool__mutmut_32, 
    'x_liteagent_tool__mutmut_33': x_liteagent_tool__mutmut_33, 
    'x_liteagent_tool__mutmut_34': x_liteagent_tool__mutmut_34, 
    'x_liteagent_tool__mutmut_35': x_liteagent_tool__mutmut_35, 
    'x_liteagent_tool__mutmut_36': x_liteagent_tool__mutmut_36, 
    'x_liteagent_tool__mutmut_37': x_liteagent_tool__mutmut_37, 
    'x_liteagent_tool__mutmut_38': x_liteagent_tool__mutmut_38, 
    'x_liteagent_tool__mutmut_39': x_liteagent_tool__mutmut_39, 
    'x_liteagent_tool__mutmut_40': x_liteagent_tool__mutmut_40, 
    'x_liteagent_tool__mutmut_41': x_liteagent_tool__mutmut_41, 
    'x_liteagent_tool__mutmut_42': x_liteagent_tool__mutmut_42, 
    'x_liteagent_tool__mutmut_43': x_liteagent_tool__mutmut_43, 
    'x_liteagent_tool__mutmut_44': x_liteagent_tool__mutmut_44, 
    'x_liteagent_tool__mutmut_45': x_liteagent_tool__mutmut_45, 
    'x_liteagent_tool__mutmut_46': x_liteagent_tool__mutmut_46
}

def liteagent_tool(*args, **kwargs):
    result = _mutmut_trampoline(x_liteagent_tool__mutmut_orig, x_liteagent_tool__mutmut_mutants, args, kwargs)
    return result 

liteagent_tool.__signature__ = _mutmut_signature(x_liteagent_tool__mutmut_orig)
x_liteagent_tool__mutmut_orig.__name__ = 'x_liteagent_tool'