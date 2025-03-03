"""
Pytest configuration for integration tests.

This module provides fixtures and setup for integration tests,
including loading environment variables from .env file.
"""

import os
import pytest
import dotenv
from pathlib import Path


# Load environment variables from .env file if it exists
def pytest_configure(config):
    """
    Load environment variables from .env file before running tests.
    
    This ensures API keys are available for integration tests.
    """
    # Find the project root (where .env file should be located)
    project_root = Path(__file__).parent.parent.parent
    dotenv_path = project_root / '.env'
    
    if dotenv_path.exists():
        print(f"Loading environment variables from {dotenv_path}")
        dotenv.load_dotenv(dotenv_path)
    else:
        print("Warning: .env file not found. Make sure API keys are set in your environment.")
    
    # Print a message if API keys are missing
    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY not found in environment variables. Tests requiring OpenAI will be skipped.")


# Import shared fixtures that will be available to all tests
from tests.integration.test_observer import ValidationObserver


@pytest.fixture
def validation_observer():
    """Create a validation observer for tests."""
    return ValidationObserver() 