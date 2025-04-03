# Task Document: Implementing TaskBased Agent in LiteAgent

## Overview
The TaskBased Agent is a specialized type of agent designed to handle long-running, complex jobs by breaking them down into smaller, manageable tasks. This agent uses a Reason/Act prompting strategy to create, manage, and execute a list of tasks while maintaining state across interactions. Unlike traditional agents that handle queries in a single turn, the TaskBased Agent can work on extended projects, keeping track of progress and methodically completing each step.

## Core Functionality
The TaskBased Agent will:
1. Break down complex queries into a list of discrete tasks
2. Track the status of each task (pending, completed, not needed, unable to complete)
3. Work through tasks systematically, updating their status as it progresses
4. Provide status updates on overall project completion
5. Handle dependencies between tasks when appropriate

## Implementation Plan

### 1. Create Task Management Tools

```python
# File: liteagent/taskbased_tools.py

"""
Tools for managing tasks in TaskBased Agents.
"""

from typing import List, Dict, Any, Optional, Literal
from .tools import BaseTool
import uuid
import time
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"
    NOT_NEEDED = "not_needed"
    UNABLE = "unable_to_complete"

class Task:
    """Represents a single task in the task list."""
    
    def __init__(self, description: str, task_id: Optional[str] = None):
        """
        Initialize a new task.
        
        Args:
            description: The task description
            task_id: Optional custom ID (default: auto-generated UUID)
        """
        self.description = description
        self.id = task_id or str(uuid.uuid4())
        self.status = TaskStatus.PENDING
        self.created_at = time.time()
        self.completed_at = None
        self.notes = ""
    
    def mark_as(self, status: TaskStatus, notes: Optional[str] = None):
        """
        Update the task status.
        
        Args:
            status: The new status
            notes: Optional notes about the status change
        """
        self.status = status
        if notes:
            self.notes = notes
        
        if status in [TaskStatus.DONE, TaskStatus.NOT_NEEDED, TaskStatus.UNABLE]:
            self.completed_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "notes": self.notes
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Task':
        """Create a Task instance from dictionary data."""
        task = Task(description=data["description"], task_id=data["id"])
        task.status = TaskStatus(data["status"])
        task.created_at = data["created_at"]
        task.completed_at = data["completed_at"]
        task.notes = data["notes"]
        return task

class TaskManager:
    """Manages a list of tasks for the agent."""
    
    def __init__(self):
        """Initialize an empty task list."""
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, description: str) -> str:
        """
        Add a new task to the list.
        
        Args:
            description: Task description
            
        Returns:
            The ID of the newly created task
        """
        task = Task(description=description)
        self.tasks[task.id] = task
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def list_tasks(self, filter_status: Optional[TaskStatus] = None) -> List[Task]:
        """
        List tasks, optionally filtered by status.
        
        Args:
            filter_status: Optional status to filter by
            
        Returns:
            List of matching tasks
        """
        if filter_status is None:
            return list(self.tasks.values())
        
        return [task for task in self.tasks.values() if task.status == filter_status]
    
    def mark_task(self, task_id: str, status: TaskStatus, notes: Optional[str] = None) -> bool:
        """
        Update a task's status.
        
        Args:
            task_id: The ID of the task to update
            status: The new status
            notes: Optional notes about the status change
            
        Returns:
            True if the task was found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        task.mark_as(status, notes)
        return True
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of task progress.
        
        Returns:
            Dictionary with task counts by status
        """
        total = len(self.tasks)
        if total == 0:
            return {
                "total": 0,
                "pending": 0,
                "done": 0,
                "not_needed": 0,
                "unable": 0,
                "percent_complete": 0
            }
        
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        done = len([t for t in self.tasks.values() if t.status == TaskStatus.DONE])
        not_needed = len([t for t in self.tasks.values() if t.status == TaskStatus.NOT_NEEDED])
        unable = len([t for t in self.tasks.values() if t.status == TaskStatus.UNABLE])
        
        # Calculate percentage complete (counting NOT_NEEDED as complete)
        completed = done + not_needed
        percent_complete = (completed / total) * 100
        
        return {
            "total": total,
            "pending": pending,
            "done": done,
            "not_needed": not_needed,
            "unable": unable,
            "percent_complete": percent_complete
        }

# Tool implementations
class AddTaskTool(BaseTool):
    """Tool to add a new task to the task list."""
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the AddTask tool.
        
        Args:
            task_manager: The task manager instance
        """
        self.task_manager = task_manager
        
        # Define the tool function
        def add_task(description: str) -> Dict[str, Any]:
            """
            Add a new task to the task list.
            
            Args:
                description: A clear description of the task to be done
                
            Returns:
                Information about the created task
            """
            task_id = self.task_manager.add_task(description)
            task = self.task_manager.get_task(task_id)
            return {
                "task_id": task_id,
                "description": task.description,
                "status": task.status,
                "message": f"Task added successfully with ID: {task_id}"
            }
        
        # Initialize the BaseTool with our function
        super().__init__(
            add_task, 
            name="AddTask",
            description="Add a new task to the task list. Use this when you need to break down a problem into steps or remember something to do later."
        )

class ListTasksTool(BaseTool):
    """Tool to list tasks in the task list."""
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the ListTasks tool.
        
        Args:
            task_manager: The task manager instance
        """
        self.task_manager = task_manager
        
        # Define the tool function
        def list_tasks(filter: str = "all") -> Dict[str, Any]:
            """
            List tasks from the task list, with optional filtering.
            
            Args:
                filter: Filter tasks by status - "all", "remaining", or "complete"
                
            Returns:
                List of tasks and summary information
            """
            # Map the filter to the appropriate TaskStatus
            status_filter = None
            if filter.lower() == "remaining":
                tasks = self.task_manager.list_tasks(TaskStatus.PENDING)
            elif filter.lower() == "complete":
                # Get both done and not needed tasks
                done_tasks = self.task_manager.list_tasks(TaskStatus.DONE)
                not_needed_tasks = self.task_manager.list_tasks(TaskStatus.NOT_NEEDED)
                tasks = done_tasks + not_needed_tasks
            else:  # "all" or any other value
                tasks = self.task_manager.list_tasks()
            
            # Convert tasks to dictionary format
            task_dicts = [task.to_dict() for task in tasks]
            
            # Get progress summary
            summary = self.task_manager.get_progress_summary()
            
            return {
                "tasks": task_dicts,
                "count": len(task_dicts),
                "filter": filter,
                "summary": summary
            }
        
        # Initialize the BaseTool with our function
        super().__init__(
            list_tasks, 
            name="ListTasks",
            description="List tasks from the task list with optional filtering. Use this to check current progress or see what tasks remain."
        )

class MarkTaskTool(BaseTool):
    """Tool to update the status of a task in the task list."""
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the MarkTask tool.
        
        Args:
            task_manager: The task manager instance
        """
        self.task_manager = task_manager
        
        # Define the tool function
        def mark_task(task_id: str, status: str, notes: str = "") -> Dict[str, Any]:
            """
            Mark a task with a specific status.
            
            Args:
                task_id: The ID of the task to update
                status: The new status - "done", "not_needed", or "unable_to_complete"
                notes: Optional notes about why the status was changed
                
            Returns:
                Information about the updated task
            """
            # Map the status string to TaskStatus enum
            status_map = {
                "done": TaskStatus.DONE,
                "not_needed": TaskStatus.NOT_NEEDED,
                "unable_to_complete": TaskStatus.UNABLE
            }
            
            if status.lower() not in status_map:
                return {
                    "success": False,
                    "message": f"Invalid status: {status}. Must be one of: done, not_needed, unable_to_complete"
                }
            
            task_status = status_map[status.lower()]
            success = self.task_manager.mark_task(task_id, task_status, notes)
            
            if not success:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found"
                }
            
            task = self.task_manager.get_task(task_id)
            
            return {
                "success": True,
                "task_id": task_id,
                "description": task.description,
                "status": task.status,
                "notes": task.notes,
                "message": f"Task marked as {status}"
            }
        
        # Initialize the BaseTool with our function
        super().__init__(
            mark_task, 
            name="MarkTask",
            description="Mark a task as done, not needed, or unable to complete. Always mark tasks when you finish them or determine they don't need to be done."
        )
```

### 2. Create the TaskBasedAgent Class

```python
# File: liteagent/taskbased_agent.py

"""
TaskBased Agent implementation for LiteAgent.

This module provides the TaskBasedAgent class, which can manage long-running
jobs by breaking them down into discrete tasks and tracking their completion.
"""

from typing import Dict, Any, List, Optional

from .agent import LiteAgent
from .taskbased_tools import TaskManager, AddTaskTool, ListTasksTool, MarkTaskTool, TaskStatus

class TaskBasedAgent(LiteAgent):
    """
    An agent that breaks down complex problems into manageable tasks and tracks their completion.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a TaskBased Agent capable of breaking down complex problems into discrete tasks.

When given a user query, your job is to:
1. Analyze the query to understand what needs to be accomplished
2. Break down the work into smaller, manageable tasks using the AddTask tool
3. Work through each task systematically
4. Mark tasks as done, not needed, or unable to complete as you progress
5. Provide clear updates on your progress

You have access to these tools:
- AddTask: Add a new task to your task list
- ListTasks: View your current tasks (can filter by all/remaining/complete)
- MarkTask: Update the status of a task (done/not_needed/unable_to_complete)

IMPORTANT WORKFLOW INSTRUCTIONS:
1. When starting a new job, ALWAYS create tasks using AddTask before beginning work
2. ALWAYS check your task list with ListTasks("remaining") before responding to the user
3. Work on ONE task at a time, and mark it complete before moving to the next
4. ALWAYS use the Reason/Act approach for each task:
   - Reason: Think about how to approach the task
   - Act: Execute the necessary actions to complete the task
5. When marking a task as done, include brief notes about what you accomplished
6. When marking a task as not_needed or unable_to_complete, explain why
7. Provide a summary of your progress in each response

Remember to track your tasks carefully and work methodically. This allows you to handle complex, multi-step problems effectively.
"""
    
    def __init__(self, model, name="TaskBasedAgent", system_prompt=None, additional_tools=None, debug=False, **kwargs):
        """
        Initialize the TaskBasedAgent.
        
        Args:
            model: The LLM model to use
            name: Name of the agent (defaults to "TaskBasedAgent")
            system_prompt: Custom system prompt (defaults to DEFAULT_SYSTEM_PROMPT)
            additional_tools: Optional additional tools beyond the task management tools
            debug: Whether to enable debug logging
            **kwargs: Additional arguments to pass to LiteAgent
        """
        self.debug = debug
        
        # Initialize the task manager
        self.task_manager = TaskManager()
        
        # Create the task management tools
        add_task_tool = AddTaskTool(self.task_manager)
        list_tasks_tool = ListTasksTool(self.task_manager)
        mark_task_tool = MarkTaskTool(self.task_manager)
        
        # Combine with any additional tools
        tools = [add_task_tool, list_tasks_tool, mark_task_tool]
        if additional_tools:
            tools.extend(additional_tools)
        
        # Initialize the LiteAgent with task management tools
        super().__init__(
            model=model,
            name=name,
            system_prompt=system_prompt or self.DEFAULT_SYSTEM_PROMPT,
            tools=tools,
            debug=debug,
            **kwargs
        )
    
    def get_task_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current task progress.
        
        Returns:
            Dictionary with task progress information
        """
        return self.task_manager.get_progress_summary()
    
    def export_tasks(self) -> List[Dict[str, Any]]:
        """
        Export all tasks as dictionaries.
        
        Returns:
            List of task dictionaries
        """
        tasks = self.task_manager.list_tasks()
        return [task.to_dict() for task in tasks]
    
    def import_tasks(self, task_data: List[Dict[str, Any]]):
        """
        Import tasks from previously exported data.
        
        Args:
            task_data: List of task dictionaries
        """
        for task_dict in task_data:
            task = self.task_manager.Task.from_dict(task_dict)
            self.task_manager.tasks[task.id] = task
```

### 3. Register the TaskBasedAgent in package __init__.py

```python
# Add to liteagent/__init__.py
from .taskbased_agent import TaskBasedAgent
```

### 4. Create Example File for the TaskBased Agent

```python
# File: examples/taskbased_agent_example.py

"""
Example demonstrating the use of the TaskBasedAgent.
"""

from liteagent import TaskBasedAgent
from liteagent.utils import check_api_keys
from examples.tools import search_database, get_weather

def run_taskbased_agent_example(model, observers=None):
    """
    Run example with the TaskBased Agent.
    
    Args:
        model (str): The model to use
        observers (list, optional): List of observers to attach to the agent
    """
    # Check for API keys
    check_api_keys()
    
    # Create a TaskBased agent with some additional tools
    agent = TaskBasedAgent(
        model=model,
        name="Project Manager Agent",
        additional_tools=[search_database, get_weather],
        observers=observers
    )
    
    # Example 1: Research Project
    print("\n=== TaskBased Agent: Research Project ===")
    response = agent.chat("I need to research the impact of climate change on coffee production worldwide. Please organize this research project for me.")
    print(f"Initial Response: {response}")
    
    # Check task list
    tasks = agent.get_task_summary()
    print(f"Tasks created: {tasks['total']}")
    
    # Continue the conversation, working through the tasks
    response = agent.chat("Great, let's start working on this. Begin with the first task.")
    print(f"Work Started Response: {response}")
    
    # Example 2: Data Analysis Project
    print("\n=== TaskBased Agent: New Project ===")
    agent = TaskBasedAgent(
        model=model,
        name="Data Analysis Agent",
        additional_tools=[search_database]
    )
    
    response = agent.chat("I have a dataset of customer purchases and I want to identify buying patterns. Can you help me analyze it?")
    print(f"Initial Response: {response}")
    
    # Continue with the analysis
    response = agent.chat("Let's assume I have the data in CSV format with columns: customer_id, product_id, purchase_date, and amount. How would you proceed?")
    print(f"Follow-up Response: {response}")
    
    # Check progress
    tasks = agent.get_task_summary()
    print(f"Task Progress: {tasks['percent_complete']}% complete ({tasks['done']} done, {tasks['pending']} pending)")

if __name__ == "__main__":
    # Use Claude, GPT-4, or other capable model that supports function calling
    model = "gpt-4o-mini"
    run_taskbased_agent_example(model)
```

## Implementation Considerations

1. **Task Persistence**: For long-running jobs, it may be important to persist task state between sessions. Consider implementing serialization/deserialization for task lists.

2. **Task Dependencies**: The current implementation treats tasks as independent, but in reality, there are often dependencies between tasks. An enhancement could involve task dependencies and ordering.

3. **Task Priority**: Implementing priority levels for tasks would help the agent focus on the most important items first.

4. **System Prompt Design**: The system prompt is crucial for guiding the agent to properly:
   - Break down problems into appropriate tasks (not too granular, not too broad)
   - Work methodically through tasks
   - Provide meaningful status updates
   - Use the Reason/Act approach for each task

5. **Error Recovery**: The agent should gracefully handle failures in task execution, potentially by creating recovery tasks or flagging tasks for user intervention.

6. **Memory Management**: For very long task lists, consider implementing pagination or archiving completed tasks to manage memory usage.

## Testing Plan

1. **Functional Testing**:
   - Test task creation, listing, and status updates
   - Test the agent's ability to break down complex problems
   - Test with multi-step processes that have dependencies
   - Verify the agent can resume work on partially completed tasks

2. **Edge Cases**:
   - Test with extremely large numbers of tasks
   - Test with ambiguous user requests
   - Test error handling when tasks cannot be completed

3. **User Experience Testing**:
   - Evaluate the clarity of progress reporting
   - Assess the agent's ability to explain its approach to each task
   - Test the user's ability to modify or reprioritize the task list mid-execution

4. **Reliability Testing**:
   - Test the agent's ability to recover from errors
   - Test persistence and restoration of task state
   - Measure completion rates for different types of complex tasks

## Future Enhancements

1. **Task Templates**: Provide pre-defined task templates for common job types (research projects, data analysis, etc.).

2. **Subtask Hierarchy**: Implement hierarchical task structures where tasks can have subtasks.

3. **Collaborative Tasks**: Allow multiple agents to work on different tasks within the same task list.

4. **User Approval Workflow**: Add functionality for the agent to request user approval before marking certain tasks complete.

5. **Progress Visualization**: Create visual representations of task progress and dependencies.

6. **Time Estimation**: Add time estimation for task completion and track actual time spent.

7. **Task Annotations**: Allow the agent to attach relevant resources, code snippets, or results to tasks.

8. **Integration with Project Management Tools**: Enable export/import with common project management formats (e.g., Jira, Trello). 