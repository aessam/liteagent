# LiteAgent Test-to-Feature Mapping Matrix

This document maps tests to features in the LiteAgent codebase to help maintain test coverage as features evolve.

## Feature Intersection Matrix

This matrix shows which combinations of features are tested together, highlighting both coverage and gaps with specific test names.

|                        | Agent<br>Core | Function<br>Calling | Observer<br>Events | Memory<br>Mgmt | Tool<br>System | Method<br>Tools | Message<br>Templates | Multi-<br>Agent | Model<br>Types |
|------------------------|---------------|---------------------|--------------------|-----------------|-----------------|-----------------|-----------------------|----------------|----------------|
| **Agent Core**         | `test_agent_initialization`<br>`test_agent_simple_chat` | `test_agent_with_function_call`<br>`test_gpt4o_mini::test_decorated_class_methods` | `test_agent_with_observer`<br>`test_observer::*_event` | `test_agent_reset_memory`<br>`test_agent_with_conversation` | `test_base_tool_*`<br>`test_gpt4o_mini::*` | `test_*_method_tool_*`<br>`test_decorated_class_methods` | `test_agent_tool_with_message_template` | `test_nested_agents`<br>`test_multi_agent::test_agent_routing` | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` |
| **Function Calling**   | `test_agent_with_function_call`<br>`test_gpt4o_mini::*` | `test_consecutive_function_calls`<br>`test_multi_step_reasoning` | `test_function_call_event`<br>`test_function_result_event` | Unit tests only<br>`test_agent::*` | `test_basic_tool_usage`<br>`test_standalone_tools` | `test_decorated_class_methods`<br>`test_class_methods_as_tools` | Unit tests only<br>No integration | `test_multi_agent::test_agent_routing`<br>`test_specialized_agents` | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` |
| **Observer Events**    | `test_agent_with_observer`<br>`test_observer::*_event` | `test_function_call_event`<br>`test_function_result_event` | `test_observer::*`<br>`test_validation::*` | Unit tests only<br>No integration | `test_validation::*`<br>`test_agent_tool_observer_propagation` | Unit tests only<br>`test_observer::*` | Unit tests only<br>No integration | `test_tree_trace_observer_multi_agent` | Unit tests only<br>`test_model_comparison` |
| **Memory Mgmt**        | `test_agent_reset_memory`<br>`test_agent_with_conversation` | Unit tests only<br>No integration | Unit tests only<br>No integration | `test_agent::*`<br>No integration | Unit tests only<br>No integration | No tests | No tests | Unit tests only<br>No integration | No tests |
| **Tool System**        | `test_base_tool_*`<br>`test_gpt4o_mini::*` | `test_basic_tool_usage`<br>`test_standalone_tools` | `test_validation::*`<br>`test_agent_tool_observer_propagation` | Unit tests only<br>No integration | `test_base_tool_*`<br>`test_agent_tool::*` | `test_instance_method_tool_*`<br>`test_decorated_class_methods` | Unit tests only<br>No integration | `test_multi_agent::*`<br>`test_specialized_agents` | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` |
| **Method Tools**       | `test_*_method_tool_*`<br>`test_decorated_class_methods` | `test_decorated_class_methods`<br>`test_class_methods_as_tools` | Unit tests only<br>`test_observer::*` | No tests | `test_instance_method_tool_*`<br>`test_decorated_class_methods` | `test_instance_method_tool_*`<br>`test_decorated_class_methods` | No tests | Unit tests only<br>No integration | `test_gpt4o_mini::test_decorated_class_methods`<br>`test_ollama_phi::test_class_methods_as_tools` |
| **Message Templates**  | `test_agent_tool_with_message_template` | Unit tests only<br>No integration | Unit tests only<br>No integration | No tests | Unit tests only<br>No integration | No tests | `test_agent_tool_with_message_template` | No tests | No tests |
| **Multi-Agent**        | `test_nested_agents`<br>`test_multi_agent::test_agent_routing` | `test_multi_agent::test_agent_routing`<br>`test_specialized_agents` | `test_tree_trace_observer_multi_agent` | Unit tests only<br>No integration | `test_multi_agent::*`<br>`test_specialized_agents` | Unit tests only<br>No integration | No tests | `test_multi_agent::*`<br>`test_parent_context_propagation` | `test_multi_agent::*` |
| **Model Types**        | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` | Unit tests only<br>`test_model_comparison` | No tests | `test_gpt4o_mini::*`<br>`test_ollama_phi::*` | `test_gpt4o_mini::test_decorated_class_methods`<br>`test_ollama_phi::test_class_methods_as_tools` | No tests | `test_multi_agent::*` | `test_model_comparison::*` |

## Model Type and Tool Support Matrix

This matrix shows which model types are tested with different tool implementations, listing the specific tests:

| Model Type | Native<br>Function<br>Calling | Text-Based<br>Function<br>Calling | Basic<br>Tools | Class<br>Method<br>Tools | Multi-Step<br>Reasoning | Observability |
|------------|-------------------------------|-----------------------------------|----------------|--------------------------|-------------------------|---------------|
| **GPT-4o-mini** | `test_gpt4o_mini::test_decorated_class_methods`<br>`test_gpt4o_mini::test_multi_step_reasoning` | N/A | `test_gpt4o_mini::*`<br>`test_model_comparison::test_basic_tool_usage` | `test_gpt4o_mini::test_decorated_class_methods` | `test_gpt4o_mini::test_multi_step_reasoning` | `test_observer::*`<br>`test_validation::*` |
| **Ollama/phi** | N/A | `test_ollama_phi::test_standalone_tools`<br>`test_ollama_phi::test_basic_tool_usage` | `test_ollama_phi::test_basic_tool_usage`<br>`test_model_comparison::test_basic_tool_usage` | `test_ollama_phi::test_class_methods_as_tools` | Limited tests<br>`test_model_comparison::test_multi_step_problem` | Limited tests<br>No direct integration tests |
| **Mock Models** | `test_agent::test_consecutive_function_calls`<br>`test_agent::test_agent_with_function_call` | `test_models::test_mock_model_function_call` | `test_tools::*`<br>`test_agent_tool::*` | `test_tools::test_instance_method_tool_*` | Limited tests<br>`test_agent::test_agent_with_conversation` | `test_observer::*`<br>`test_validation_observer` |

## Critical Intersections and Gaps

The following critical feature intersections have limited or no test coverage:

1. **Memory × Different Model Types**: No specific tests verify memory handling across different model types
2. **Message Templates × Function Calling**: Limited testing of message templates with function calls
3. **Observer Events × Text-Based Function Calling**: Limited validation that observers correctly track text-based function calls
4. **Method Tools × Multi-Agent Communication**: Limited testing of class method tools in multi-agent scenarios
5. **Memory Management × Tool System**: Limited verification of memory persistence across tool executions

## Feature-to-Test Reference

| Feature/Component | Unit Tests | Integration Tests |
|-------------------|------------|-------------------|
| **Agent Initialization** | ✅ test_agent.py::test_agent_initialization<br>✅ test_agent_tool.py::test_agent_tool_creation<br>✅ test_observer.py::test_agent_initialized_event | ✅ test_gpt4o_mini.py<br>✅ test_ollama_phi.py |
| **Agent Chat** | ✅ test_agent.py::test_agent_simple_chat<br>✅ test_agent_tool.py::test_agent_tool_execution | ✅ test_gpt4o_mini.py<br>✅ test_ollama_phi.py |
| **Function Calling** | ✅ test_agent.py::test_agent_with_function_call<br>✅ test_agent.py::test_consecutive_function_calls<br>✅ test_agent.py::test_repeated_function_call_prevention<br>✅ test_observer.py::test_function_call_event<br>✅ test_observer.py::test_function_result_event<br>✅ test_models.py::test_function_calling_model_response_extraction<br>✅ test_models.py::test_function_calling_model_content_extraction | ✅ test_gpt4o_mini.py::test_decorated_class_methods<br>✅ test_gpt4o_mini.py::test_multi_step_reasoning<br>✅ test_ollama_phi.py::test_standalone_tools |
| **Observer Events** | ✅ test_agent.py::test_agent_with_observer<br>✅ test_agent_tool.py::test_agent_tool_observer_propagation<br>✅ test_observer.py::test_agent_event_base<br>✅ test_observer.py::test_model_response_event<br>✅ test_observer.py::test_user_message_event<br>✅ test_observer.py::test_function_call_event | ✅ test_observer.py |
| **Memory Management** | ✅ test_agent.py::test_agent_reset_memory<br>✅ test_agent.py::test_agent_with_conversation | ❌ *No dedicated integration tests* |
| **Tool System** | ✅ test_tools.py::test_base_tool_initialization<br>✅ test_tools.py::test_base_tool_execute<br>✅ test_tools.py::test_base_tool_to_function_definition | ✅ test_gpt4o_mini.py<br>✅ test_ollama_phi.py |
| **Method Tools** | ✅ test_tools.py::test_instance_method_tool_with_instance_method<br>✅ test_tools.py::test_instance_method_tool_with_class_method<br>✅ test_tools.py::test_instance_method_tool_with_static_method | ✅ test_gpt4o_mini.py::test_decorated_class_methods<br>✅ test_ollama_phi.py::test_class_methods_as_tools |
| **Message Templates** | ✅ test_agent_tool.py::test_agent_tool_with_message_template | ❌ *No dedicated integration tests* |
| **Multi-Agent Communication** | ✅ test_agent.py::test_nested_agents<br>✅ test_agent.py::test_parent_context_propagation | ✅ test_multi_agent.py::test_specialized_agents<br>✅ test_multi_agent.py::test_agent_routing |
| **Agent Tracing** | ✅ test_observer.py::test_tree_trace_observer_tracking<br>✅ test_observer.py::test_tree_trace_observer_tree_visualization<br>✅ test_observer.py::test_tree_trace_observer_multi_agent | ❌ *No dedicated integration tests* |
| **Model Interface** | ✅ test_models.py::test_mock_model_text_response<br>✅ test_models.py::test_mock_model_function_call<br>✅ test_models.py::test_multiple_responses | ✅ test_model_comparison.py |
| **Model Detection** | ✅ test_models.py::test_function_calling_model_detection<br>✅ test_models.py::test_create_model_interface_factory | ❌ *No dedicated integration tests* |
| **Validation Patterns** | ✅ test_observer.py::test_validation_observer<br>✅ test_observer.py::test_sequence_validation_observer | ✅ test_validation.py::test_specific_tool_parameter_validation<br>✅ test_validation.py::test_call_sequence_validation<br>✅ test_validation.py::test_conditional_validation |
| **Model Comparison** | ❌ *No dedicated unit tests* | ✅ test_model_comparison.py::test_basic_tool_usage<br>✅ test_model_comparison.py::test_complex_tool_usage<br>✅ test_model_comparison.py::test_multi_step_problem |
| **Different Model Support** | ❌ *No dedicated unit tests* | ✅ test_gpt4o_mini.py<br>✅ test_ollama_phi.py |

## Test Coverage by Component

| Component | Coverage % | Main Test Files | Key Missing Tests |
|-----------|------------|----------------|-------------------|
| agent.py | 78% | test_agent.py<br>test_multi_agent.py | Error recovery strategies |
| agent_tool.py | 65% | test_agent_tool.py | Message template edge cases, error conditions |
| memory.py | 68% | test_agent.py | Direct memory manipulation, context restoration |
| models.py | 70% | test_models.py<br>test_model_comparison.py | Error handling for API failures |
| observer.py | 75% | test_observer.py<br>test_validation.py | Console and file observer tests |
| tools.py | 70% | test_tools.py | Complex tool combinations, error recovery |
| utils.py | 45% | - | Most utility functions lack direct tests |

## Integration Test Coverage

| Integration Test | Purpose | Models Tested | Key Features Tested |
|------------------|---------|--------------|---------------------|
| test_gpt4o_mini.py | Tests with GPT-4o-mini | gpt-4o-mini | Function calling, multi-step reasoning, tool combinations |
| test_ollama_phi.py | Tests with Ollama Phi | ollama/phi | Basic tool usage, class methods as tools, standalone tools |
| test_multi_agent.py | Tests multi-agent functionality | gpt-4o-mini | Specialized agents, agent routing, agent communication |
| test_model_comparison.py | Compares different models | gpt-4o-mini, ollama/phi | Basic tools, complex tools, reasoning |
| test_validation.py | Tests validation patterns | gpt-4o-mini | Tool parameters, call sequences, conditional validation |
| test_observer.py | Tests observer functionality | - | Function call recording, validation assertions |

## Test Coverage Improvement Priorities

Based on the feature intersection matrix, these are the highest priority areas for improved test coverage:

1. **Observer Events × Text-Based Function Calling**: Add integration tests that verify observers correctly track function calls with text-based models
2. **Memory Management × Different Model Types**: Create tests that verify memory handling works consistently across model types
3. **Message Templates × Function Calling**: Add tests for using message templates with function calling
4. **Memory Management × Tool System**: Verify memory persistence properly works with tool execution 
5. **Method Tools × Multi-Agent**: Test class method tools in multi-agent scenarios

## Maintenance Guidelines

When adding new features:
1. Add corresponding test cases to both unit and integration test suites
2. Update this matrix to reflect new test-to-feature mappings and intersections
3. Prioritize test coverage for critical feature combinations

When modifying existing features:
1. Verify that existing tests still pass
2. Update tests as needed to match modified functionality
3. Update this matrix if test names or feature categorizations change 