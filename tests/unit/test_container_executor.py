"""
Tests for container_executor.py
"""

import os
import json
import tempfile
import shutil
from unittest import mock
import subprocess
import pytest

from liteagent.container_executor import (
    ContainerExecutor,
    DockerExecutor,
    PodmanExecutor,
    ContainerFactory
)


class DummyContainerExecutor(ContainerExecutor):
    """Dummy implementation for testing abstract class methods"""
    
    def prepare_container(self):
        pass
        
    def execute_code(self, code):
        return {"result": "dummy"}, "logs", True
        
    def cleanup(self):
        pass


class TestContainerExecutor:
    """Test cases for the ContainerExecutor class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        # Create a test file in the test directory
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_init(self):
        """Test initialization of the container executor."""
        executor = DummyContainerExecutor(
            source_directory=self.test_dir,
            authorized_imports=["numpy", "pandas"],
            memory_limit="2g",
            timeout=60,
            network_enabled=True
        )
        
        # Check that the parameters were set correctly
        assert executor.source_directory == os.path.abspath(self.test_dir)
        assert executor.authorized_imports == ["numpy", "pandas"]
        assert executor.memory_limit == "2g"
        assert executor.timeout == 60
        assert executor.network_enabled is True
        
    def test_init_defaults(self):
        """Test initialization with default values."""
        executor = DummyContainerExecutor(source_directory=self.test_dir)
        
        # Check that the default parameters were set correctly
        assert executor.source_directory == os.path.abspath(self.test_dir)
        assert "os" in executor.authorized_imports
        assert "sys" in executor.authorized_imports
        assert executor.memory_limit == "1g"
        assert executor.timeout == 30
        assert executor.network_enabled is False
        
    def test_create_shadow_copy(self):
        """Test creating a shadow copy of the source directory."""
        executor = DummyContainerExecutor(source_directory=self.test_dir)
        
        # Create a shadow copy
        shadow_dir = executor.create_shadow_copy()
        
        try:
            # Check that the shadow directory was created
            assert os.path.exists(shadow_dir)
            # Check that the test file was copied
            assert os.path.exists(os.path.join(shadow_dir, "test_file.txt"))
            # Check that the content of the file is the same
            with open(os.path.join(shadow_dir, "test_file.txt"), "r") as f:
                assert f.read() == "test content"
        finally:
            # Clean up
            if os.path.exists(shadow_dir):
                shutil.rmtree(shadow_dir)
                
    def test_context_manager(self):
        """Test using the container executor as a context manager."""
        executor = DummyContainerExecutor(source_directory=self.test_dir)
        
        # Mock the methods
        executor.create_shadow_copy = mock.MagicMock(return_value="/tmp/shadow")
        executor.prepare_container = mock.MagicMock()
        executor.cleanup = mock.MagicMock()
        
        # Use the context manager
        with executor as e:
            assert e is executor
            
        # Check that the methods were called
        executor.create_shadow_copy.assert_called_once()
        executor.prepare_container.assert_called_once()
        executor.cleanup.assert_called_once()


@pytest.mark.skipif(shutil.which("docker") is None, reason="Docker is not installed")
class TestDockerExecutor:
    """Test cases for the DockerExecutor class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        # Create a test file in the test directory
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_init(self):
        """Test initialization of the Docker executor."""
        executor = DockerExecutor(
            source_directory=self.test_dir,
            authorized_imports=["numpy", "pandas"],
            memory_limit="2g",
            timeout=60,
            network_enabled=True,
            image="python:3.8-slim"
        )
        
        # Check that the parameters were set correctly
        assert executor.source_directory == os.path.abspath(self.test_dir)
        assert executor.authorized_imports == ["numpy", "pandas"]
        assert executor.memory_limit == "2g"
        assert executor.timeout == 60
        assert executor.network_enabled is True
        assert executor.image == "python:3.8-slim"
        
    @mock.patch("subprocess.run")
    def test_prepare_container(self, mock_run):
        """Test preparing the Docker container."""
        executor = DockerExecutor(source_directory=self.test_dir)
        
        # Mock the subprocess.run calls
        mock_run.return_value = mock.Mock(returncode=0)
        
        # Call prepare_container
        executor.prepare_container()
        
        # Check that the methods were called
        assert mock_run.call_count >= 2
        
    @mock.patch("subprocess.run")
    def test_execute_code_success(self, mock_run):
        """Test executing code successfully in the Docker container."""
        executor = DockerExecutor(source_directory=self.test_dir)
        
        # Create a shadow directory
        executor.create_shadow_copy = mock.MagicMock(return_value=self.test_dir)
        executor.shadow_dir = self.test_dir
        
        # Mock successful execution
        mock_process = mock.Mock()
        mock_process.stdout = "Process output"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Create a result file
        result_file = os.path.join(self.test_dir, "execution_result.json")
        with open(result_file, "w") as f:
            json.dump({"success": True, "output": "Hello, world!"}, f)
        
        try:
            # Execute code
            result, logs, success = executor.execute_code('print("Hello, world!")')
            
            # Check that the result is correct
            assert success is True
            assert logs == "Process output"
            assert result["output"] == "Hello, world!"
        finally:
            # Clean up
            if os.path.exists(result_file):
                os.remove(result_file)
                
    @mock.patch("subprocess.run")
    def test_execute_code_failure(self, mock_run):
        """Test executing code with errors in the Docker container."""
        executor = DockerExecutor(source_directory=self.test_dir)
        
        # Create a shadow directory
        executor.create_shadow_copy = mock.MagicMock(return_value=self.test_dir)
        executor.shadow_dir = self.test_dir
        
        # Mock failed execution
        mock_process = mock.Mock()
        mock_process.stdout = ""
        mock_process.stderr = "Error message"
        mock_process.returncode = 1
        mock_run.return_value = mock_process
        
        # Execute code
        result, logs, success = executor.execute_code('print(undefined_variable)')
        
        # Check that the result is correct
        assert success is False
        assert logs == "Error message"
        assert "error" in result
        
    @mock.patch("subprocess.run")
    def test_execute_code_timeout(self, mock_run):
        """Test executing code with a timeout in the Docker container."""
        executor = DockerExecutor(source_directory=self.test_dir)
        
        # Create a shadow directory
        executor.create_shadow_copy = mock.MagicMock(return_value=self.test_dir)
        executor.shadow_dir = self.test_dir
        
        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="docker run", timeout=30)
        
        # Execute code
        result, logs, success = executor.execute_code('import time; time.sleep(100)')
        
        # Check that the result is correct
        assert success is False
        assert "timeout" in logs.lower()
        assert "error" in result
        
    @mock.patch("subprocess.run")
    def test_cleanup(self, mock_run):
        """Test cleaning up resources after execution."""
        executor = DockerExecutor(source_directory=self.test_dir)
        
        # Set up the executor
        executor.container_id = "test_container_id"
        executor.shadow_dir = tempfile.mkdtemp()
        
        try:
            # Call cleanup
            executor.cleanup()
            
            # Check that the container was removed
            mock_run.assert_called_with(
                ["docker", "rm", "-f", "liteagent-test_container_id"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Check that the shadow directory was removed
            assert not os.path.exists(executor.shadow_dir)
            assert executor.shadow_dir is None
        finally:
            # Clean up if the test fails
            if executor.shadow_dir and os.path.exists(executor.shadow_dir):
                shutil.rmtree(executor.shadow_dir)


@pytest.mark.skipif(shutil.which("podman") is None, reason="Podman is not installed")
class TestPodmanExecutor:
    """Test cases for the PodmanExecutor class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        # Create a test file in the test directory
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_init(self):
        """Test initialization of the Podman executor."""
        executor = PodmanExecutor(
            source_directory=self.test_dir,
            authorized_imports=["numpy", "pandas"],
            memory_limit="2g",
            timeout=60,
            network_enabled=True,
            image="python:3.8-slim"
        )
        
        # Check that the parameters were set correctly
        assert executor.source_directory == os.path.abspath(self.test_dir)
        assert executor.authorized_imports == ["numpy", "pandas"]
        assert executor.memory_limit == "2g"
        assert executor.timeout == 60
        assert executor.network_enabled is True
        assert executor.image == "python:3.8-slim"
        
    @mock.patch("subprocess.run")
    def test_prepare_container(self, mock_run):
        """Test preparing the Podman container."""
        executor = PodmanExecutor(source_directory=self.test_dir)
        
        # Mock the subprocess.run calls
        mock_run.return_value = mock.Mock(returncode=0)
        
        # Call prepare_container
        executor.prepare_container()
        
        # Check that the methods were called
        assert mock_run.call_count >= 2
        
    @mock.patch("subprocess.run")
    def test_execute_code_success(self, mock_run):
        """Test executing code successfully in the Podman container."""
        executor = PodmanExecutor(source_directory=self.test_dir)
        
        # Create a shadow directory
        executor.create_shadow_copy = mock.MagicMock(return_value=self.test_dir)
        executor.shadow_dir = self.test_dir
        
        # Mock successful execution
        mock_process = mock.Mock()
        mock_process.stdout = "Process output"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Create a result file
        result_file = os.path.join(self.test_dir, "execution_result.json")
        with open(result_file, "w") as f:
            json.dump({"success": True, "output": "Hello, world!"}, f)
        
        try:
            # Execute code
            result, logs, success = executor.execute_code('print("Hello, world!")')
            
            # Check that the result is correct
            assert success is True
            assert logs == "Process output"
            assert result["output"] == "Hello, world!"
        finally:
            # Clean up
            if os.path.exists(result_file):
                os.remove(result_file)


class TestContainerFactory:
    """Test cases for the ContainerFactory class."""
    
    def test_create_container_docker(self):
        """Test creating a Docker container."""
        with mock.patch("liteagent.container_executor.DockerExecutor") as mock_docker:
            # Create a Docker container
            ContainerFactory.create_container(container_type="docker")
            
            # Check that DockerExecutor was called
            mock_docker.assert_called_once()
            
    def test_create_container_podman(self):
        """Test creating a Podman container."""
        with mock.patch("liteagent.container_executor.PodmanExecutor") as mock_podman:
            # Create a Podman container
            ContainerFactory.create_container(container_type="podman")
            
            # Check that PodmanExecutor was called
            mock_podman.assert_called_once()
            
    def test_create_container_invalid(self):
        """Test creating a container with an invalid type."""
        with pytest.raises(ValueError):
            ContainerFactory.create_container(container_type="invalid")
            
    def test_create_container_with_template(self):
        """Test creating a container with a template."""
        with mock.patch("liteagent.container_executor.PodmanExecutor") as mock_podman:
            # Create a Podman container with the ML template
            ContainerFactory.create_container(container_type="podman", template="ml")
            
            # Check that PodmanExecutor was called with the right parameters
            args, kwargs = mock_podman.call_args
            assert kwargs["memory_limit"] == "4g"
            assert "numpy" in kwargs["authorized_imports"]
            assert "pandas" in kwargs["authorized_imports"]
            assert kwargs["timeout"] == 120
            
    def test_create_container_with_custom_config(self):
        """Test creating a container with custom configuration."""
        with mock.patch("liteagent.container_executor.PodmanExecutor") as mock_podman:
            # Create a Podman container with custom configuration
            ContainerFactory.create_container(
                container_type="podman",
                memory_limit="8g",
                timeout=300,
                network_enabled=True
            )
            
            # Check that PodmanExecutor was called with the right parameters
            args, kwargs = mock_podman.call_args
            assert kwargs["memory_limit"] == "8g"
            assert kwargs["timeout"] == 300
            assert kwargs["network_enabled"] is True
            
    def test_create_container_template_override(self):
        """Test creating a container with a template and overriding some parameters."""
        with mock.patch("liteagent.container_executor.DockerExecutor") as mock_docker:
            # Create a Docker container with the secure template but override timeout
            ContainerFactory.create_container(
                container_type="docker",
                template="secure",
                timeout=60
            )
            
            # Check that DockerExecutor was called with the right parameters
            args, kwargs = mock_docker.call_args
            assert kwargs["memory_limit"] == "512m"  # From template
            assert kwargs["timeout"] == 60  # Overridden