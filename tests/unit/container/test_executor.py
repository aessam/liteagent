"""
Tests for the ContainerExecutor class and its subclasses.

These tests verify the functionality of the ContainerExecutor classes,
focusing on proper initialization, shadow directory creation,
and code execution within containers.
"""

import os
import tempfile
import shutil
import pytest
from unittest import mock
import subprocess
from pathlib import Path

from liteagent.container.executor import (
    ContainerExecutor,
    DockerExecutor,
    PodmanExecutor,
    ContainerFactory
)

class TestContainerExecutor:
    """Test cases for the ContainerExecutor base class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        # Create some test files in the directory
        with open(os.path.join(temp_dir, "test.txt"), "w") as f:
            f.write("Test file content")
        with open(os.path.join(temp_dir, "test.py"), "w") as f:
            f.write("print('Hello, world!')")
        # Create a subdirectory with files
        os.makedirs(os.path.join(temp_dir, "subdir"))
        with open(os.path.join(temp_dir, "subdir", "test.txt"), "w") as f:
            f.write("Test file in subdirectory")
            
        yield temp_dir
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def mock_container_executor(self, temp_dir):
        """Create a mock ContainerExecutor for testing."""
        class MockContainerExecutor(ContainerExecutor):
            def prepare_container(self):
                self.shadow_directory = self.create_shadow_copy(self.source_directory)
                self.container_id = "mock_container_id"
            
            def execute_code(self, code):
                return ("mock_result", "mock_logs", True)
            
            def cleanup(self):
                if self.shadow_directory:
                    self.cleanup_shadow_directory(self.shadow_directory)
                    self.shadow_directory = None
                self.container_id = None
        
        return MockContainerExecutor(source_directory=temp_dir)
    
    def test_init_with_valid_directory(self, temp_dir, mock_container_executor):
        """Test initialization with a valid directory."""
        assert mock_container_executor.source_directory == os.path.abspath(temp_dir)
        assert mock_container_executor.container_type == "podman"  # Default
        assert mock_container_executor.memory_limit == "1g"
        assert mock_container_executor.timeout == 30
        assert not mock_container_executor.network_enabled
        assert mock_container_executor.authorized_imports == ["os", "sys", "json", "re", "collections", "datetime"]
    
    def test_init_with_invalid_directory(self, temp_dir):
        """Test initialization with an invalid directory."""
        # Create a mock class that inherits from ContainerExecutor to avoid abstract method issue
        class TestExecutor(ContainerExecutor):
            def prepare_container(self): pass
            def execute_code(self, code): pass
            def cleanup(self): pass
        
        with pytest.raises(ValueError, match="Source directory does not exist"):
            TestExecutor(source_directory="/nonexistent/directory")
    
    def test_create_shadow_copy(self, mock_container_executor, temp_dir):
        """Test creation of shadow directory."""
        shadow_dir = mock_container_executor.create_shadow_copy(temp_dir)
        try:
            # Check that the shadow directory exists
            assert os.path.isdir(shadow_dir)
            
            # Check that the files were copied
            assert os.path.isfile(os.path.join(shadow_dir, "test.txt"))
            assert os.path.isfile(os.path.join(shadow_dir, "test.py"))
            
            # Check the subdirectory
            assert os.path.isdir(os.path.join(shadow_dir, "subdir"))
            assert os.path.isfile(os.path.join(shadow_dir, "subdir", "test.txt"))
            
            # Check file contents
            with open(os.path.join(shadow_dir, "test.txt"), "r") as f:
                assert f.read() == "Test file content"
        finally:
            # Clean up the shadow directory
            mock_container_executor.cleanup_shadow_directory(shadow_dir)
    
    def test_cleanup_shadow_directory(self, mock_container_executor, temp_dir):
        """Test cleanup of shadow directory."""
        shadow_dir = mock_container_executor.create_shadow_copy(temp_dir)
        assert os.path.isdir(shadow_dir)
        
        mock_container_executor.cleanup_shadow_directory(shadow_dir)
        assert not os.path.exists(shadow_dir)

class TestDockerExecutor:
    """Test cases for the DockerExecutor class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        with open(os.path.join(temp_dir, "test.py"), "w") as f:
            f.write("print('Hello, world!')")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @mock.patch("subprocess.run")
    def test_init_with_docker_available(self, mock_run, temp_dir):
        """Test initialization when Docker is available."""
        mock_run.return_value = mock.Mock(returncode=0, stdout="Docker version 20.10.8")
        executor = DockerExecutor(source_directory=temp_dir)
        assert executor.container_type == "docker"
        mock_run.assert_called_once()
    
    @mock.patch("subprocess.run")
    def test_init_with_docker_unavailable(self, mock_run, temp_dir):
        """Test initialization when Docker is not available."""
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'docker'")
        with pytest.raises(RuntimeError, match="Docker is not installed"):
            DockerExecutor(source_directory=temp_dir)
    
    @mock.patch("subprocess.run")
    def test_prepare_container(self, mock_run, temp_dir):
        """Test container preparation."""
        # Mock docker --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="Docker version 20.10.8")
        
        executor = DockerExecutor(source_directory=temp_dir)
        
        # Reset the mock to prepare for the next calls
        mock_run.reset_mock()
        
        # Mock the docker run command
        mock_run.return_value = mock.Mock(returncode=0, stdout="container_id", stderr="")
        
        # Create shadow directory with a real path
        with mock.patch.object(executor, 'create_shadow_copy') as mock_shadow:
            shadow_dir = tempfile.mkdtemp()
            mock_shadow.return_value = shadow_dir
            
            try:
                executor.prepare_container()
                
                # Check that docker run was called
                assert mock_run.call_count >= 1
                
                # Verify that the container ID was set
                assert executor.container_id == "container_id"
                
                # Verify that shadow directory was created
                assert executor.shadow_directory == shadow_dir
            finally:
                executor.cleanup_shadow_directory(shadow_dir)
                
    @mock.patch("subprocess.run")
    def test_execute_code(self, mock_run, temp_dir):
        """Test code execution in container."""
        # Mock docker --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="Docker version 20.10.8")
        
        executor = DockerExecutor(source_directory=temp_dir)
        
        # Set container ID and shadow directory
        executor.container_id = "test_container"
        executor.shadow_directory = temp_dir
        
        # Mock the docker exec command
        mock_run.reset_mock()
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout="\n__LITEAGENT_RESULT_JSON__\n" + 
                   '{"success": true, "result": "Hello, world!", "output": "Hello, world!\\n"}',
            stderr=""
        )
        
        # Execute some test code
        result, logs, success = executor.execute_code('print("Hello, world!")')
        
        # Check the result
        assert result == "Hello, world!"
        assert "Hello, world!" in logs
        assert success is True
        
        # Verify that docker exec was called
        assert mock_run.call_count == 1
        
    @mock.patch("subprocess.run")
    def test_cleanup(self, mock_run, temp_dir):
        """Test cleanup of Docker resources."""
        # Mock docker --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="Docker version 20.10.8")
        
        executor = DockerExecutor(source_directory=temp_dir)
        
        # Set container ID and shadow directory
        executor.container_id = "test_container"
        executor.shadow_directory = temp_dir
        
        # Reset mock for cleanup calls
        mock_run.reset_mock()
        
        # Clean up resources
        executor.cleanup()
        
        # Verify that docker stop and docker rm were called
        assert mock_run.call_count == 2
        
        # Check that container ID and shadow directory were reset
        assert executor.container_id is None
        assert executor.shadow_directory is None

class TestPodmanExecutor:
    """Test cases for the PodmanExecutor class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        with open(os.path.join(temp_dir, "test.py"), "w") as f:
            f.write("print('Hello, world!')")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @mock.patch("subprocess.run")
    def test_init_with_podman_available(self, mock_run, temp_dir):
        """Test initialization when Podman is available."""
        mock_run.return_value = mock.Mock(returncode=0, stdout="podman version 3.4.0")
        executor = PodmanExecutor(source_directory=temp_dir)
        assert executor.container_type == "podman"
        mock_run.assert_called_once()
    
    @mock.patch("subprocess.run")
    def test_init_with_podman_unavailable(self, mock_run, temp_dir):
        """Test initialization when Podman is not available."""
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'podman'")
        with pytest.raises(RuntimeError, match="Podman is not installed"):
            PodmanExecutor(source_directory=temp_dir)
    
    @mock.patch("subprocess.run")
    def test_prepare_container(self, mock_run, temp_dir):
        """Test container preparation."""
        # Mock podman --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="podman version 3.4.0")
        
        executor = PodmanExecutor(source_directory=temp_dir)
        
        # Reset the mock to prepare for the next calls
        mock_run.reset_mock()
        
        # Mock the podman run command
        mock_run.return_value = mock.Mock(returncode=0, stdout="container_id", stderr="")
        
        # Create shadow directory with a real path
        with mock.patch.object(executor, 'create_shadow_copy') as mock_shadow:
            shadow_dir = tempfile.mkdtemp()
            mock_shadow.return_value = shadow_dir
            
            try:
                executor.prepare_container()
                
                # Check that podman run was called
                assert mock_run.call_count >= 1
                
                # Verify that the container ID was set
                assert executor.container_id == "container_id"
                
                # Verify that shadow directory was created
                assert executor.shadow_directory == shadow_dir
            finally:
                executor.cleanup_shadow_directory(shadow_dir)
                
    @mock.patch("subprocess.run")
    def test_execute_code(self, mock_run, temp_dir):
        """Test code execution in container."""
        # Mock podman --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="podman version 3.4.0")
        
        executor = PodmanExecutor(source_directory=temp_dir)
        
        # Set container ID and shadow directory
        executor.container_id = "test_container"
        executor.shadow_directory = temp_dir
        
        # Mock the podman exec command
        mock_run.reset_mock()
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout="\n__LITEAGENT_RESULT_JSON__\n" + 
                   '{"success": true, "result": "Hello, world!", "output": "Hello, world!\\n"}',
            stderr=""
        )
        
        # Execute some test code
        result, logs, success = executor.execute_code('print("Hello, world!")')
        
        # Check the result
        assert result == "Hello, world!"
        assert "Hello, world!" in logs
        assert success is True
        
        # Verify that podman exec was called
        assert mock_run.call_count == 1
        
    @mock.patch("subprocess.run")
    def test_cleanup(self, mock_run, temp_dir):
        """Test cleanup of Podman resources."""
        # Mock podman --version
        mock_run.return_value = mock.Mock(returncode=0, stdout="podman version 3.4.0")
        
        executor = PodmanExecutor(source_directory=temp_dir)
        
        # Set container ID and shadow directory
        executor.container_id = "test_container"
        executor.shadow_directory = temp_dir
        
        # Reset mock for cleanup calls
        mock_run.reset_mock()
        
        # Clean up resources
        executor.cleanup()
        
        # Verify that podman stop and podman rm were called
        assert mock_run.call_count == 2
        
        # Check that container ID and shadow directory were reset
        assert executor.container_id is None
        assert executor.shadow_directory is None

class TestContainerFactory:
    """Test cases for the ContainerFactory."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @mock.patch("liteagent.container.executor.DockerExecutor")
    def test_create_docker_container(self, mock_docker, temp_dir):
        """Test creation of a Docker container."""
        mock_docker.return_value = "mock_docker_executor"
        executor = ContainerFactory.create_container(
            source_directory=temp_dir,
            container_type="docker",
            template="default"
        )
        assert executor == "mock_docker_executor"
        mock_docker.assert_called_once()
    
    @mock.patch("liteagent.container.executor.PodmanExecutor")
    def test_create_podman_container(self, mock_podman, temp_dir):
        """Test creation of a Podman container."""
        mock_podman.return_value = "mock_podman_executor"
        executor = ContainerFactory.create_container(
            source_directory=temp_dir,
            container_type="podman",
            template="default"
        )
        assert executor == "mock_podman_executor"
        mock_podman.assert_called_once()
    
    @mock.patch("liteagent.container.executor.PodmanExecutor")
    def test_create_container_with_custom_config(self, mock_podman, temp_dir):
        """Test creation of a container with custom configuration."""
        mock_podman.return_value = "mock_podman_executor"
        executor = ContainerFactory.create_container(
            source_directory=temp_dir,
            container_type="podman",
            template="secure",
            memory_limit="2g",
            network_enabled=True
        )
        assert executor == "mock_podman_executor"
        
        # Check that the custom config was applied
        _, kwargs = mock_podman.call_args
        assert kwargs["memory_limit"] == "2g"
        assert kwargs["network_enabled"] is True
        assert kwargs["read_only"] is True  # From template
    
    @mock.patch("liteagent.container.executor.PodmanExecutor")
    def test_create_container_with_invalid_template(self, mock_podman, temp_dir):
        """Test creation of a container with an invalid template."""
        mock_podman.return_value = "mock_podman_executor"
        executor = ContainerFactory.create_container(
            source_directory=temp_dir,
            container_type="podman",
            template="nonexistent"
        )
        assert executor == "mock_podman_executor"
        
        # Check that the default template was used
        _, kwargs = mock_podman.call_args
        assert kwargs["memory_limit"] == "1g"  # From default template
    
    def test_create_container_with_invalid_type(self, temp_dir):
        """Test creation of a container with an invalid type."""
        with pytest.raises(ValueError, match="Unsupported container type"):
            ContainerFactory.create_container(
                source_directory=temp_dir,
                container_type="invalid"
            )