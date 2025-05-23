"""
Integration tests for the ContainerExecutor functionality.

These tests verify that ContainerExecutor can properly set up containers
and execute code within them.
"""

import os
import pytest
import tempfile
import shutil
from pathlib import Path
import subprocess

from liteagent.container import ContainerExecutor, ContainerFactory, PodmanExecutor, DockerExecutor

@pytest.fixture
def test_directory():
    """Create a temporary directory with test files."""
    temp_dir = tempfile.mkdtemp()
    # Create some test files
    with open(os.path.join(temp_dir, "test_file.txt"), "w") as f:
        f.write("Hello, world!")
        
    # Create a Python script
    with open(os.path.join(temp_dir, "test_script.py"), "w") as f:
        f.write("""
def add(a, b):
    return a + b

result = add(2, 3)
print(f"The result is {result}")

# Store the result for the container executor
_liteagent_result = result
""")
        
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.mark.integration
def test_container_factory_create():
    """Test ContainerFactory creation with default settings."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # We're just testing initialization, not actual container creation, so mock the container type check
        try:
            container = ContainerFactory.create_container(
                source_directory=temp_dir, 
                template="default"
            )
            assert isinstance(container, (DockerExecutor, PodmanExecutor))
            assert container.source_directory == os.path.abspath(temp_dir)
            assert container.memory_limit == "1g"
            assert not container.network_enabled
        except (RuntimeError, FileNotFoundError):
            # Skip if Docker/Podman is not available
            pytest.skip("Neither Docker nor Podman available for testing")

@pytest.mark.integration
def test_container_select_type():
    """Test container type selection."""
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Try Docker first
            container = ContainerFactory.create_container(
                source_directory=temp_dir, 
                container_type="docker"
            )
            assert isinstance(container, DockerExecutor)
        except (RuntimeError, FileNotFoundError):
            try:
                # Try Podman if Docker not available
                container = ContainerFactory.create_container(
                    source_directory=temp_dir, 
                    container_type="podman"
                )
                assert isinstance(container, PodmanExecutor)
            except (RuntimeError, FileNotFoundError):
                # Skip if neither is available
                pytest.skip("Neither Docker nor Podman available for testing")

@pytest.mark.integration
@pytest.mark.slow
def test_execute_code_in_container(test_directory):
    """Test executing code in a container."""
    # Check for Docker or Podman availability
    container_type = None
    for ctype in ["podman", "docker"]:
        try:
            result = subprocess.run(
                [ctype, "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                check=False
            )
            if result.returncode == 0:
                container_type = ctype
                break
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    
    if not container_type:
        pytest.skip("No container runtime available for testing")
    
    # Create and prepare the container
    container = ContainerFactory.create_container(
        source_directory=test_directory,
        container_type=container_type,
        template="default"
    )
    
    try:
        container.prepare_container()
        
        # Execute a simple code snippet
        code = """
import os

# List files in the current directory
files = os.listdir(".")
print(f"Files in directory: {files}")

# Read the content of test_file.txt
with open("test_file.txt", "r") as f:
    content = f.read()
print(f"Content of test_file.txt: {content}")

# Execute the test_script.py
with open("test_script.py", "r") as f:
    exec(f.read())

# Set the final result
_liteagent_result = {
    "files": files,
    "file_content": content,
    "calculation_result": result
}
"""
        
        result, logs, success = container.execute_code(code)
        
        # Check that the execution was successful
        assert success, f"Code execution failed: {logs}"
        
        # Verify the result contains the expected data
        assert isinstance(result, dict)
        assert "files" in result
        assert "test_file.txt" in result["files"]
        assert "test_script.py" in result["files"]
        assert result["file_content"] == "Hello, world!"
        assert result["calculation_result"] == 5
        
        # Check logs
        assert "Files in directory:" in logs
        assert "Content of test_file.txt: Hello, world!" in logs
        assert "The result is 5" in logs
        
    finally:
        # Clean up
        container.cleanup()