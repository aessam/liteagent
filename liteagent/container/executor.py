"""
ContainerExecutor module for secure code execution in containers.

This module provides classes for executing code within Docker or Podman containers,
implementing security measures to protect the host system while allowing LiteCodeAgent
to work with files through a shadow copy mechanism.
"""

import os
import shutil
import tempfile
import subprocess
import json
import uuid
import logging
from typing import Any, Dict, List, Optional, Tuple, Union, Set
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

class ContainerExecutor(ABC):
    """
    Base class for executing LLM-generated Python code in a secure container environment.
    
    This is an abstract class that defines the interface for container executors.
    Specific implementations should be made for Docker, Podman, or other container technologies.
    """
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: Optional[List[str]] = None,
                 container_type: str = "podman",  # Default to podman
                 memory_limit: str = "1g",
                 cpu_limit: str = "1",
                 timeout: int = 30,
                 network_enabled: bool = False,
                 read_only: bool = True):
        """
        Initialize the container executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            container_type: Type of container technology to use ("docker" or "podman")
            memory_limit: Memory limit for the container
            cpu_limit: CPU limit for the container (cores)
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
            read_only: Whether to mount the source directory as read-only
        """
        self.source_directory = os.path.abspath(source_directory)
        if not os.path.exists(self.source_directory):
            raise ValueError(f"Source directory does not exist: {self.source_directory}")
            
        self.authorized_imports = authorized_imports or ["os", "sys", "json", "re", "collections", "datetime"]
        self.container_type = container_type.lower()
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.timeout = timeout
        self.network_enabled = network_enabled
        self.read_only = read_only
        
        # Container ID will be set when the container is created
        self.container_id = None
        
        # Shadow directory will be created when prepare_container is called
        self.shadow_directory = None
        
        logger.debug(f"Initialized {self.__class__.__name__} for {self.container_type} with "
                     f"memory={self.memory_limit}, cpu={self.cpu_limit}, timeout={self.timeout}s, "
                     f"network={'enabled' if self.network_enabled else 'disabled'}")
        
    def create_shadow_copy(self, src_dir: str) -> str:
        """
        Create a shadow copy of the source directory.
        
        Args:
            src_dir: Source directory to copy
            
        Returns:
            Path to the shadow directory
        """
        # Create a temporary directory for the shadow copy
        shadow_dir = tempfile.mkdtemp(prefix="liteagent_shadow_")
        logger.debug(f"Creating shadow copy of {src_dir} at {shadow_dir}")
        
        try:
            # Create the directory structure
            for root, dirs, files in os.walk(src_dir):
                # Get the relative path from the source directory
                rel_path = os.path.relpath(root, src_dir)
                if rel_path == ".":
                    rel_path = ""
                    
                # Create the directory structure
                for directory in dirs:
                    os.makedirs(os.path.join(shadow_dir, rel_path, directory), exist_ok=True)
                    
                # Copy files
                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(shadow_dir, rel_path, file)
                    try:
                        shutil.copy2(src_file, dst_file)
                    except (shutil.SameFileError, OSError) as e:
                        logger.warning(f"Could not copy file {src_file}: {str(e)}")
            
            return shadow_dir
        except Exception as e:
            # Clean up the shadow directory if an error occurs
            self.cleanup_shadow_directory(shadow_dir)
            raise RuntimeError(f"Error creating shadow copy: {str(e)}")
    
    def cleanup_shadow_directory(self, shadow_dir: str) -> None:
        """
        Clean up the shadow directory.
        
        Args:
            shadow_dir: Path to the shadow directory
        """
        if os.path.exists(shadow_dir):
            try:
                shutil.rmtree(shadow_dir)
                logger.debug(f"Removed shadow directory: {shadow_dir}")
            except Exception as e:
                logger.error(f"Error removing shadow directory {shadow_dir}: {str(e)}")
    
    @abstractmethod
    def prepare_container(self) -> None:
        """
        Set up the container with necessary dependencies.
        
        This method should be implemented by subclasses to create a container
        with the appropriate configuration.
        """
        pass
    
    @abstractmethod
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """
        Execute code in the container and return result, logs, and final status.
        
        Args:
            code: Python code to execute
            
        Returns:
            Tuple of (result object, logs, success status)
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Clean up resources after execution.
        
        This should remove the container and any temporary files.
        """
        pass

class DockerExecutor(ContainerExecutor):
    """
    Executor that uses Docker to run code in a container.
    """
    
    def __init__(self, source_directory: str, **kwargs):
        """
        Initialize DockerExecutor with appropriate settings.
        
        Args:
            source_directory: Directory to be mounted in the container
            **kwargs: Additional arguments to pass to ContainerExecutor
        """
        super().__init__(source_directory, container_type="docker", **kwargs)
        # Check if Docker is available
        try:
            result = subprocess.run(
                ["docker", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                check=False
            )
            if result.returncode != 0:
                raise RuntimeError("Docker is not available on this system")
            logger.debug(f"Docker version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError("Docker is not installed on this system")
    
    def prepare_container(self) -> None:
        """Set up Docker container with necessary dependencies."""
        # Create shadow directory
        self.shadow_directory = self.create_shadow_copy(self.source_directory)
        
        # Create a unique name for the container
        container_name = f"liteagent_docker_{uuid.uuid4().hex[:8]}"
        
        # Create the container
        cmd = [
            "docker", "run",
            "-d",  # Detached mode
            "--name", container_name,
            "--memory", self.memory_limit,
            "--cpus", self.cpu_limit,
            f"--network={'bridge' if self.network_enabled else 'none'}",
            "-v", f"{self.shadow_directory}:/workspace:{'ro' if self.read_only else 'rw'}",
            "-w", "/workspace",
            "python:3.9-slim"
        ]
        
        # Run the container creation command
        try:
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
            self.container_id = result.stdout.strip()
            logger.info(f"Created Docker container: {self.container_id} (name: {container_name})")
            
            # Install required packages inside the container
            if self.authorized_imports:
                self._install_packages()
        except subprocess.CalledProcessError as e:
            self.cleanup_shadow_directory(self.shadow_directory)
            raise RuntimeError(f"Failed to create Docker container: {str(e)}\nOutput: {e.stderr}")
    
    def _install_packages(self) -> None:
        """Install authorized packages in the container."""
        if not self.container_id:
            raise RuntimeError("Container not created yet. Call prepare_container first.")
        
        # Convert package list to pip-installable format
        packages = " ".join(self.authorized_imports)
        
        try:
            result = subprocess.run(
                ["docker", "exec", self.container_id, "pip", "install", "--no-cache-dir"] + self.authorized_imports,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            logger.debug(f"Installed packages in container: {packages}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install some packages: {str(e)}\nOutput: {e.stderr}")
    
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """Execute code in the Docker container."""
        if not self.container_id:
            raise RuntimeError("Container not created yet. Call prepare_container first.")
        
        # Save code to a temporary file in the shadow directory
        code_file = os.path.join(self.shadow_directory, "_liteagent_code.py")
        with open(code_file, "w") as f:
            f.write(code)
        
        # Create a wrapper script that captures output and serializes the result
        wrapper_code = """
import sys
import json
import traceback
from io import StringIO

# Redirect stdout/stderr to capture output
out = StringIO()
sys.stdout = out
sys.stderr = out

try:
    # Execute the user code
    result = None
    with open('_liteagent_code.py', 'r') as f:
        code = f.read()
    
    # Add a global variable to collect the final result
    code += "\\n\\n# Store the final result in _liteagent_result for serialization"
    namespace = {}
    exec(code, namespace)
    
    # Get the result from the namespace if available
    result = namespace.get('_liteagent_result', None)
    
    # Try to serialize the result
    try:
        json_result = json.dumps({
            'success': True,
            'result': result,
            'output': out.getvalue()
        })
        print("\\n__LITEAGENT_RESULT_JSON__\\n" + json_result)
    except Exception as e:
        print("\\n__LITEAGENT_RESULT_JSON__\\n" + json.dumps({
            'success': True,
            'result': str(result),
            'output': out.getvalue(),
            'serialization_error': str(e)
        }))
except Exception as e:
    traceback.print_exc()
    # Report failure
    print("\\n__LITEAGENT_RESULT_JSON__\\n" + json.dumps({
        'success': False,
        'error': str(e),
        'traceback': traceback.format_exc(),
        'output': out.getvalue()
    }))
"""
        
        wrapper_file = os.path.join(self.shadow_directory, "_liteagent_wrapper.py")
        with open(wrapper_file, "w") as f:
            f.write(wrapper_code)
        
        # Execute the wrapper script in the container with timeout
        cmd = [
            "docker", "exec",
            "-w", "/workspace",
            self.container_id,
            "timeout", str(self.timeout),
            "python", "_liteagent_wrapper.py"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False  # Don't raise error on non-zero exit
            )
            
            # Parse the output to extract the JSON result
            output = result.stdout + result.stderr
            result_marker = "__LITEAGENT_RESULT_JSON__\n"
            if result_marker in output:
                json_text = output.split(result_marker)[1]
                try:
                    result_data = json.loads(json_text)
                    return (
                        result_data.get('result'), 
                        result_data.get('output', ''), 
                        result_data.get('success', False)
                    )
                except json.JSONDecodeError:
                    return (
                        None,
                        f"Error decoding result JSON: {json_text}",
                        False
                    )
            else:
                return (
                    None,
                    f"Execution failed or timed out: {output}",
                    False
                )
        except Exception as e:
            return (
                None,
                f"Error executing code: {str(e)}",
                False
            )
    
    def cleanup(self) -> None:
        """Clean up Docker resources."""
        # Stop and remove the container
        if self.container_id:
            try:
                subprocess.run(
                    ["docker", "stop", self.container_id],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False
                )
                subprocess.run(
                    ["docker", "rm", self.container_id],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False
                )
                logger.info(f"Removed Docker container: {self.container_id}")
            except Exception as e:
                logger.error(f"Error removing Docker container: {str(e)}")
            
            self.container_id = None
        
        # Clean up the shadow directory
        if self.shadow_directory:
            self.cleanup_shadow_directory(self.shadow_directory)
            self.shadow_directory = None

class PodmanExecutor(ContainerExecutor):
    """
    Executor that uses Podman to run code in a container.
    """
    
    def __init__(self, source_directory: str, **kwargs):
        """
        Initialize PodmanExecutor with appropriate settings.
        
        Args:
            source_directory: Directory to be mounted in the container
            **kwargs: Additional arguments to pass to ContainerExecutor
        """
        super().__init__(source_directory, container_type="podman", **kwargs)
        # Check if Podman is available
        try:
            result = subprocess.run(
                ["podman", "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                check=False
            )
            if result.returncode != 0:
                raise RuntimeError("Podman is not available on this system")
            logger.debug(f"Podman version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError("Podman is not installed on this system")
    
    def prepare_container(self) -> None:
        """Set up Podman container with necessary dependencies."""
        # Create shadow directory
        self.shadow_directory = self.create_shadow_copy(self.source_directory)
        
        # Create a unique name for the container
        container_name = f"liteagent_podman_{uuid.uuid4().hex[:8]}"
        
        # Create the container
        cmd = [
            "podman", "run",
            "-d",  # Detached mode
            "--name", container_name,
            "--memory", self.memory_limit,
            "--cpus", self.cpu_limit,
            f"--network={'bridge' if self.network_enabled else 'none'}",
            "-v", f"{self.shadow_directory}:/workspace:{'ro' if self.read_only else 'rw,Z'}",
            "-w", "/workspace",
            "python:3.9-slim"
        ]
        
        # Run the container creation command
        try:
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                check=True
            )
            self.container_id = result.stdout.strip()
            logger.info(f"Created Podman container: {self.container_id} (name: {container_name})")
            
            # Install required packages inside the container
            if self.authorized_imports:
                self._install_packages()
        except subprocess.CalledProcessError as e:
            self.cleanup_shadow_directory(self.shadow_directory)
            raise RuntimeError(f"Failed to create Podman container: {str(e)}\nOutput: {e.stderr}")
    
    def _install_packages(self) -> None:
        """Install authorized packages in the container."""
        if not self.container_id:
            raise RuntimeError("Container not created yet. Call prepare_container first.")
        
        # Convert package list to pip-installable format
        packages = " ".join(self.authorized_imports)
        
        try:
            result = subprocess.run(
                ["podman", "exec", self.container_id, "pip", "install", "--no-cache-dir"] + self.authorized_imports,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            logger.debug(f"Installed packages in container: {packages}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install some packages: {str(e)}\nOutput: {e.stderr}")
    
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """Execute code in the Podman container."""
        if not self.container_id:
            raise RuntimeError("Container not created yet. Call prepare_container first.")
        
        # Save code to a temporary file in the shadow directory
        code_file = os.path.join(self.shadow_directory, "_liteagent_code.py")
        with open(code_file, "w") as f:
            f.write(code)
        
        # Create a wrapper script that captures output and serializes the result
        wrapper_code = """
import sys
import json
import traceback
from io import StringIO

# Redirect stdout/stderr to capture output
out = StringIO()
sys.stdout = out
sys.stderr = out

try:
    # Execute the user code
    result = None
    with open('_liteagent_code.py', 'r') as f:
        code = f.read()
    
    # Add a global variable to collect the final result
    code += "\\n\\n# Store the final result in _liteagent_result for serialization"
    namespace = {}
    exec(code, namespace)
    
    # Get the result from the namespace if available
    result = namespace.get('_liteagent_result', None)
    
    # Try to serialize the result
    try:
        json_result = json.dumps({
            'success': True,
            'result': result,
            'output': out.getvalue()
        })
        print("\\n__LITEAGENT_RESULT_JSON__\\n" + json_result)
    except Exception as e:
        print("\\n__LITEAGENT_RESULT_JSON__\\n" + json.dumps({
            'success': True,
            'result': str(result),
            'output': out.getvalue(),
            'serialization_error': str(e)
        }))
except Exception as e:
    traceback.print_exc()
    # Report failure
    print("\\n__LITEAGENT_RESULT_JSON__\\n" + json.dumps({
        'success': False,
        'error': str(e),
        'traceback': traceback.format_exc(),
        'output': out.getvalue()
    }))
"""
        
        wrapper_file = os.path.join(self.shadow_directory, "_liteagent_wrapper.py")
        with open(wrapper_file, "w") as f:
            f.write(wrapper_code)
        
        # Execute the wrapper script in the container with timeout
        cmd = [
            "podman", "exec",
            "-w", "/workspace",
            self.container_id,
            "timeout", str(self.timeout),
            "python", "_liteagent_wrapper.py"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False  # Don't raise error on non-zero exit
            )
            
            # Parse the output to extract the JSON result
            output = result.stdout + result.stderr
            result_marker = "__LITEAGENT_RESULT_JSON__\n"
            if result_marker in output:
                json_text = output.split(result_marker)[1]
                try:
                    result_data = json.loads(json_text)
                    return (
                        result_data.get('result'), 
                        result_data.get('output', ''), 
                        result_data.get('success', False)
                    )
                except json.JSONDecodeError:
                    return (
                        None,
                        f"Error decoding result JSON: {json_text}",
                        False
                    )
            else:
                return (
                    None,
                    f"Execution failed or timed out: {output}",
                    False
                )
        except Exception as e:
            return (
                None,
                f"Error executing code: {str(e)}",
                False
            )
    
    def cleanup(self) -> None:
        """Clean up Podman resources."""
        # Stop and remove the container
        if self.container_id:
            try:
                subprocess.run(
                    ["podman", "stop", self.container_id],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False
                )
                subprocess.run(
                    ["podman", "rm", self.container_id],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False
                )
                logger.info(f"Removed Podman container: {self.container_id}")
            except Exception as e:
                logger.error(f"Error removing Podman container: {str(e)}")
            
            self.container_id = None
        
        # Clean up the shadow directory
        if self.shadow_directory:
            self.cleanup_shadow_directory(self.shadow_directory)
            self.shadow_directory = None

class ContainerFactory:
    """Factory for creating secure container environments with standardized configurations."""
    
    @staticmethod
    def create_container(source_directory: str, container_type: str = "podman", template: str = "default", **custom_config) -> ContainerExecutor:
        """
        Create a container with a predefined template and optional custom configurations.
        
        Args:
            source_directory: Directory to be mounted in the container
            container_type: "docker" or "podman"
            template: Predefined template ("default", "secure", "ml", "web", etc.)
            **custom_config: Custom configurations to override template defaults
            
        Returns:
            Configured ContainerExecutor instance
        """
        # Templates provide sensible defaults for different use cases
        templates = {
            "default": {
                "memory_limit": "1g",
                "cpu_limit": "1",
                "timeout": 30,
                "network_enabled": False,
                "read_only": True,
                "authorized_imports": ["os", "sys", "json", "re", "collections", "datetime"]
            },
            "secure": {
                "memory_limit": "512m",
                "cpu_limit": "0.5",
                "timeout": 15,
                "network_enabled": False,
                "read_only": True,
                "authorized_imports": ["json", "re", "collections"]
            },
            "ml": {
                "memory_limit": "4g",
                "cpu_limit": "2",
                "timeout": 120,
                "network_enabled": False,
                "read_only": True,
                "authorized_imports": ["numpy", "pandas", "sklearn", "matplotlib"]
            },
            "web": {
                "memory_limit": "2g",
                "cpu_limit": "1",
                "timeout": 60,
                "network_enabled": True,  # Allow network for web tasks
                "read_only": True,
                "authorized_imports": ["requests", "beautifulsoup4", "urllib3", "aiohttp"]
            }
            # Add more templates as needed
        }
        
        # Get base configuration from template
        if template not in templates:
            logger.warning(f"Template '{template}' not found, using 'default'")
            template = "default"
            
        config = templates[template].copy()
        
        # Override with custom configurations
        config.update(custom_config)
        
        # Create and return the executor
        if container_type.lower() == "docker":
            return DockerExecutor(source_directory=source_directory, **config)
        elif container_type.lower() == "podman":
            return PodmanExecutor(source_directory=source_directory, **config)
        else:
            raise ValueError(f"Unsupported container type: {container_type}")