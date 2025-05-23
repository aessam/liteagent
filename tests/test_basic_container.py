"""
Basic tests for ContainerExecutor that don't require the full test environment.
"""

import os
import tempfile
import shutil
from unittest import mock
import pytest

# Import ContainerExecutor directly from the module
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from liteagent.container_executor import ContainerExecutor


class DummyContainerExecutor(ContainerExecutor):
    """Dummy implementation for testing abstract class methods"""
    
    def prepare_container(self):
        pass
        
    def execute_code(self, code):
        return {"result": "dummy"}, "logs", True
        
    def cleanup(self):
        pass


def test_init():
    """Test initialization of the container executor."""
    test_dir = tempfile.mkdtemp()
    try:
        # Create a test file in the test directory
        with open(os.path.join(test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
        executor = DummyContainerExecutor(test_dir)
        assert executor.source_directory == os.path.abspath(test_dir)
        assert executor.authorized_imports == ["os", "sys", "json", "re", "collections", "datetime"]
        assert executor.memory_limit == "1g"
        assert executor.timeout == 30
        assert executor.network_enabled is False
        assert executor.container_id is None
        assert executor.shadow_dir is None
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        
        
def test_init_with_custom_params():
    """Test initialization with custom parameters."""
    test_dir = tempfile.mkdtemp()
    try:
        executor = DummyContainerExecutor(
            test_dir,
            authorized_imports=["numpy", "pandas"],
            memory_limit="2g",
            timeout=60,
            network_enabled=True
        )
        assert executor.source_directory == os.path.abspath(test_dir)
        assert executor.authorized_imports == ["numpy", "pandas"]
        assert executor.memory_limit == "2g"
        assert executor.timeout == 60
        assert executor.network_enabled is True
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        
def test_create_shadow_copy():
    """Test shadow copy creation."""
    test_dir = tempfile.mkdtemp()
    try:
        # Create a test file in the test directory
        with open(os.path.join(test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
        executor = DummyContainerExecutor(test_dir)
        shadow_dir = executor.create_shadow_copy()
        
        # Check that shadow directory was created
        assert os.path.exists(shadow_dir)
        assert executor.shadow_dir == shadow_dir
        
        # Check that the test file was copied
        shadow_file_path = os.path.join(shadow_dir, "test_file.txt")
        assert os.path.exists(shadow_file_path)
        
        with open(shadow_file_path, "r") as f:
            content = f.read()
            assert content == "test content"
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        if executor.shadow_dir and os.path.exists(executor.shadow_dir):
            shutil.rmtree(executor.shadow_dir)
        
def test_context_manager():
    """Test context manager interface."""
    test_dir = tempfile.mkdtemp()
    try:
        executor = DummyContainerExecutor(test_dir)
        
        # Mock methods
        executor.prepare_container = mock.MagicMock()
        executor.cleanup = mock.MagicMock()
        executor.create_shadow_copy = mock.MagicMock(return_value="/tmp/shadow")
        
        # Use context manager
        with executor as exec_ctx:
            assert exec_ctx == executor
            
        # Verify methods were called
        executor.create_shadow_copy.assert_called_once()
        executor.prepare_container.assert_called_once()
        executor.cleanup.assert_called_once()
    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)