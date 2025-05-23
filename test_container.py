"""
Simple standalone test for the ContainerExecutor.
"""

import os
import tempfile
import shutil
from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from unittest import mock


class ContainerExecutor(ABC):
    """
    Abstract base class for executing code in a container environment.
    
    This class defines the interface for container executors and provides
    common utility methods.
    """
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: List[str] = None,
                 memory_limit: str = "1g",
                 timeout: int = 30,
                 network_enabled: bool = False):
        """
        Initialize the container executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            memory_limit: Memory limit for the container
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
        """
        self.source_directory = os.path.abspath(source_directory)
        self.authorized_imports = authorized_imports or ["os", "sys", "json", "re", "collections", "datetime"]
        self.memory_limit = memory_limit
        self.timeout = timeout
        self.network_enabled = network_enabled
        self.container_id = None
        self.shadow_dir = None
        
    def create_shadow_copy(self) -> str:
        """
        Create a shadow copy of the source directory to avoid modifying original files.
        
        Returns:
            Path to the shadow directory
        """
        # Create a temporary directory for the shadow copy
        shadow_dir = tempfile.mkdtemp(prefix="liteagent_shadow_")
        
        try:
            # Copy files from source directory to shadow directory
            if os.path.exists(self.source_directory):
                for item in os.listdir(self.source_directory):
                    src_path = os.path.join(self.source_directory, item)
                    dst_path = os.path.join(shadow_dir, item)
                    
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                
            # Save the shadow directory path
            self.shadow_dir = shadow_dir
            return shadow_dir
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(shadow_dir):
                shutil.rmtree(shadow_dir)
            raise ValueError(f"Failed to create shadow copy: {str(e)}")
    
    @abstractmethod
    def prepare_container(self) -> None:
        """Set up the container with necessary dependencies"""
        pass
        
    @abstractmethod
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """
        Execute code in the container and return result, logs, and status.
        
        Args:
            code: Python code to execute
            
        Returns:
            Tuple containing (result, logs, success_status)
        """
        pass
        
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources after execution"""
        pass
    
    def __enter__(self):
        """Context manager entry point"""
        if not self.shadow_dir:
            self.create_shadow_copy()
        self.prepare_container()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.cleanup()


class DummyContainerExecutor(ContainerExecutor):
    """Dummy implementation for testing abstract class methods"""
    
    def prepare_container(self):
        print("Preparing container...")
        
    def execute_code(self, code):
        print("Executing code...")
        return {"result": "dummy"}, "logs", True
        
    def cleanup(self):
        print("Cleaning up...")


def test_container_executor():
    """Test basic functionality of ContainerExecutor"""
    print("Creating test directory...")
    test_dir = tempfile.mkdtemp()
    
    try:
        # Create a test file in the test directory
        print("Creating test file...")
        with open(os.path.join(test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
        # Initialize executor
        print("Initializing executor...")
        executor = DummyContainerExecutor(test_dir)
        
        # Check initialization
        print("Checking initialization...")
        assert executor.source_directory == os.path.abspath(test_dir)
        assert "os" in executor.authorized_imports
        assert executor.memory_limit == "1g"
        assert executor.timeout == 30
        assert executor.network_enabled is False
        
        # Test shadow copy
        print("Testing shadow copy creation...")
        shadow_dir = executor.create_shadow_copy()
        assert os.path.exists(shadow_dir)
        
        # Check that the file was copied
        shadow_file = os.path.join(shadow_dir, "test_file.txt")
        assert os.path.exists(shadow_file)
        with open(shadow_file) as f:
            content = f.read()
            assert content == "test content"
        
        # Test context manager
        print("Testing context manager...")
        real_prepare = executor.prepare_container
        real_cleanup = executor.cleanup
        
        executor.prepare_container = mock.MagicMock()
        executor.cleanup = mock.MagicMock()
        
        with executor as ctx:
            assert ctx == executor
        
        executor.prepare_container.assert_called_once()
        executor.cleanup.assert_called_once()
        
        # Restore real methods
        executor.prepare_container = real_prepare
        executor.cleanup = real_cleanup
        
        # Clean up shadow directory
        if executor.shadow_dir and os.path.exists(executor.shadow_dir):
            shutil.rmtree(executor.shadow_dir)
        
        print("All tests passed!")
        return True
    
    finally:
        # Clean up test directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    success = test_container_executor()
    print(f"Test {'succeeded' if success else 'failed'}")