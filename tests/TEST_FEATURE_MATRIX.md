# LiteAgent Test-to-Feature Mapping Matrix

This document maps tests to features in the LiteAgent codebase to help maintain test coverage as features evolve.

## Feature-to-Test Matrix

| Feature/Component | Agent Core | Agent Tools | Observer | Memory | Models | Tools System |
|-------------------|------------|-------------|----------|--------|--------|--------------|
| **Agent Initialization** | test_agent_initialization | test_agent_tool_creation | test_agent_initialized_event | - | - | - |
| **Agent Chat** | test_agent_simple_chat | test_agent_tool_execution | - | - | - | - |
| **Function Calling** | test_agent_with_function_call<br>test_consecutive_function_calls<br>test_repeated_function_call_prevention | - | test_function_call_event<br>test_function_result_event | - | test_function_calling_model_response_extraction<br>test_function_calling_model_content_extraction | - |
| **Observer Events** | test_agent_with_observer | test_agent_tool_observer_propagation | test_agent_event_base<br>test_model_response_event<br>test_user_message_event<br>test_function_call_event | - | - | - |
| **Memory Management** | test_agent_reset_memory<br>test_agent_with_conversation | - | - | - | - | - |
| **Tool System** | - | - | - | - | - | test_base_tool_initialization<br>test_base_tool_execute<br>test_base_tool_to_function_definition |
| **Method Tools** | - | - | - | - | - | test_instance_method_tool_with_instance_method<br>test_instance_method_tool_with_class_method<br>test_instance_method_tool_with_static_method |
| **Message Templates** | - | test_agent_tool_with_message_template | - | - | - | - |
| **Multi-Agent Communication** | - | test_nested_agents<br>test_parent_context_propagation | test_tree_trace_observer_multi_agent | - | - | - |
| **Agent Tracing** | - | - | test_tree_trace_observer_tracking<br>test_tree_trace_observer_tree_visualization | - | - | - |
| **Model Interface** | - | - | - | - | test_mock_model_text_response<br>test_mock_model_function_call<br>test_multiple_responses | - |
| **Model Detection** | - | - | - | - | test_function_calling_model_detection<br>test_create_model_interface_factory | - |

## Test Coverage by Component

| Component | Coverage % | Main Test Files | Key Missing Tests |
|-----------|------------|----------------|-------------------|
| agent.py | 76% | test_agent.py | Error handling, edge cases |
| agent_tool.py | 59% | test_agent_tool.py | Message template edge cases, error conditions |
| memory.py | 68% | test_agent.py | Direct memory manipulation, context restoration |
| models.py | 65% | test_models.py | Additional model types, error handling |
| observer.py | 70% | test_observer.py | Console and file observer tests |
| tools.py | 62% | test_tools.py | StaticMethodTool, function registration |
| utils.py | 45% | - | Most utility functions lack direct tests |

## Test Coverage Improvement Priorities

1. **utils.py (45%)**: Create dedicated test file and coverage for utility functions
2. **agent_tool.py (59%)**: Add tests for error handling and edge cases
3. **tools.py (62%)**: Complete tests for all tool types and registration
4. **models.py (65%)**: Add tests for additional model types and error scenarios
5. **memory.py (68%)**: Test direct memory manipulation and serialization

## Maintenance Guidelines

When adding new features:
1. Add corresponding test cases
2. Update this matrix to reflect new test-to-feature mappings
3. Prioritize test coverage for critical components

When modifying existing features:
1. Verify that existing tests still pass
2. Update tests as needed to match modified functionality
3. Update this matrix if test names or feature categorizations change 