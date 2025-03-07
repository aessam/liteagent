"""
This module has been moved to the examples directory.

Please import from examples.basic_examples or examples.tools instead.

Examples:
    from examples.basic_examples import run_examples
    run_examples(model="gpt-3.5-turbo")
    
    # Or for standalone tools
    from examples.tools import get_weather, add_numbers
"""

import warnings

warnings.warn(
    "The examples module has been moved to the examples directory. "
    "Please import from examples.basic_examples or examples.tools instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import functions from the new location for backward compatibility
from examples.basic_examples import (
    run_examples, 
    run_class_methods_example,
    run_custom_agents_example,
    run_simplified_tools_example
)

# Import tools for backward compatibility
from examples.tools import (
    get_weather,
    add_numbers,
    search_database,
    calculate_area,
    ToolsForAgents,
    SimplifiedToolsForAgents
)