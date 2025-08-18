# Consolidated Integration Tests

This directory contains consolidated integration tests for the LiteAgent framework. The goal is to reduce code duplication and make the tests more maintainable.

## Benefits of Consolidation

1. **Code Reduction**: Reduces total lines of test code by centralizing common patterns
2. **Maintenance Simplification**: Changes only need to be made in one place
3. **Consistent Testing**: Same validation approaches used across all models
4. **Better Coverage**: Tests run against all supported models by default
5. **Easier Onboarding**: New developers can understand the test structure more easily

## Approach

These tests are designed to test the same functionality across multiple models using pytest's powerful fixture system. Key features:

1. **Model Parametrization**: Tests are parametrized with different models (OpenAI, Anthropic, Groq, Ollama)
2. **Flexible Validation**: Tests handle different model behaviors (e.g., some models return None responses)
3. **Graceful Error Handling**: Tests skip gracefully when models are not available or return unusable responses
4. **Shared Fixtures**: Common fixtures in conftest.py handle setup and teardown

## Test Structure

Each test file follows this structure:

- **Test Class**: Contains tests for a specific capability (e.g., standalone tools, class method tools)
- **Fixtures**: Provide test-specific configuration (tools, prompts, etc.)
- **Test Methods**: Individual tests that run against all configured models

## Cleanup Process

After implementing consolidated tests, follow the cleanup process outlined in CLEANUP_PLAN.md:

1. Verify all functionality is covered in the consolidated tests
2. Run consolidated tests to ensure they pass
3. Gradually remove redundant model-specific test files
4. Update CI pipeline to use consolidated tests

## Running Tests

To run all consolidated tests:
```
python -m pytest tests/integration/consolidated
```

To run a specific test file:
```
python -m pytest tests/integration/consolidated/test_standalone_tools.py
```

To run a specific test:
```
python -m pytest tests/integration/consolidated/test_standalone_tools.py::TestStandaloneTools::test_weather_tool
```

## Adding New Tests

To add a new test:

1. Add a fixture to provide any required test-specific configuration
2. Implement test methods that use the configured_agent fixture
3. Use ValidationTestHelper methods to validate tool usage
4. Handle None responses and model-specific exceptions

## Migrating Existing Tests

When migrating model-specific tests to the consolidated approach:

1. Identify the key functionality being tested
2. Create appropriate fixtures for configuration
3. Implement test methods that work with all models
4. Add proper error handling for model-specific issues
5. Verify the consolidated test provides the same coverage
6. Remove the original test file after thorough testing 