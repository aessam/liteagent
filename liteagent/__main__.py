#!/usr/bin/env python
"""
Main entry point for running LiteAgent when using 'python -m liteagent'.
This enables users to access the command-line functionality via module execution.
"""

from .cli import main

if __name__ == "__main__":
    main() 