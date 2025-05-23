# Container Execution for LiteCodeAgent

This package provides the container execution capabilities for LiteCodeAgent. It enables code execution in secure container environments using either Docker or Podman.

## Features

- **Secure Execution**: All code runs in isolated containers with configurable resource limits
- **Shadow Copies**: Source directories are shadow-copied to protect original files
- **Multiple Container Options**: Supports both Docker and Podman as container runtimes
- **Security Controls**: Memory limits, CPU limits, network isolation, and execution timeouts
- **Standardized Templates**: Pre-configured templates for different types of workloads

## Core Components

### ContainerExecutor

`ContainerExecutor` is the base abstract class that defines the interface for container execution:

```python
from liteagent.container import ContainerExecutor

class MyCustomExecutor(ContainerExecutor):
    def prepare_container(self):
        # Custom implementation
        pass
        
    def execute_code(self, code):
        # Custom implementation
        pass
        
    def cleanup(self):
        # Custom implementation
        pass
```

### DockerExecutor and PodmanExecutor

Ready-to-use implementations for Docker and Podman container runtimes:

```python
from liteagent.container import DockerExecutor, PodmanExecutor

# Use Docker
executor = DockerExecutor(
    source_directory="/path/to/source",
    memory_limit="2g",
    timeout=60,
    network_enabled=False
)

# Use Podman
executor = PodmanExecutor(
    source_directory="/path/to/source",
    memory_limit="1g",
    timeout=30,
    network_enabled=False
)
```

### ContainerFactory

A factory class for creating container executors with standardized templates:

```python
from liteagent.container import ContainerFactory

# Create a container with default template
executor = ContainerFactory.create_container(
    source_directory="/path/to/source",
    container_type="podman"  # or "docker"
)

# Create a container with specific template
executor = ContainerFactory.create_container(
    source_directory="/path/to/source",
    container_type="podman",
    template="ml"  # Pre-configured for machine learning tasks
)

# Create a container with custom configuration
executor = ContainerFactory.create_container(
    source_directory="/path/to/source",
    container_type="podman",
    template="default",
    memory_limit="4g",
    timeout=120,
    network_enabled=True,
    authorized_imports=["numpy", "pandas", "matplotlib"]
)
```

## Template Types

The ContainerFactory supports several pre-configured templates:

- **default**: Basic configuration with essential imports
- **secure**: Minimal configuration with restricted imports for security-critical tasks
- **ml**: Configuration for machine learning tasks with relevant imports
- **web**: Configuration for web-related tasks with network access and relevant imports

## Usage Example

```python
from liteagent.container import ContainerFactory

# Create a container
container = ContainerFactory.create_container(
    source_directory="/path/to/source",
    container_type="podman",
    template="default"
)

try:
    # Prepare the container
    container.prepare_container()
    
    # Execute code in the container
    result, logs, success = container.execute_code("""
    import os
    
    # List files in directory
    files = os.listdir(".")
    
    # Store the result for return
    _liteagent_result = files
    """)
    
    if success:
        print(f"Execution successful. Result: {result}")
        print(f"Logs: {logs}")
    else:
        print(f"Execution failed: {logs}")
        
finally:
    # Clean up resources
    container.cleanup()
```

## Security Considerations

- All code executes in isolated containers
- Shadow copies protect original files from modification
- Resource limits prevent resource exhaustion
- Network is disabled by default
- Read-only mounting prevents file modifications by default
- Automatic cleanup of resources after execution