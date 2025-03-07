"""
This module has been moved to the cli directory.

Please import from cli.commands instead.

Examples:
    from cli.commands import main
    main()
"""

import warnings

warnings.warn(
    "The CLI module has been moved to the cli directory. "
    "Please import from cli.commands instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import functions from the new location for backward compatibility
from cli.commands import (
    main,
    parse_arguments,
    show_version,
    run_examples,
    handle_model_prefix
) 