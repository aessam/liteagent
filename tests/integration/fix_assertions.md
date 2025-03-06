# Guide to Fixing Problematic Assertions in Tests

This guide outlines how to identify and fix logically flawed assertions in the test suite.

## Common Problematic Assertions

### 1. String Matching Assertions

**Problem**: Assertions that check if specific strings are in responses are brittle and unreliable.

```python
# PROBLEMATIC:
assert any(term in response.lower() for term in ["tokyo", "weather", "temperature"])
assert any(str(num) in response for num in ["42", "forty-two", "forty two"])
```

**Solution**: Use structured validation with the ValidationObserver:

```python
# BETTER:
parsed_response = validation_observer.parse_response(response)
assert "city" in parsed_response, "Response should contain city information"
assert parsed_response["city"].lower() == "tokyo", "City should be Tokyo"

# OR:
validation_observer.assert_response_contains_structure(
    response, 
    {"city": "Tokyo", "temperature": object}
)
```

### 2. Conditional Assertions

**Problem**: Assertions inside if-conditions can result in tests that pass without validating anything.

```python
# PROBLEMATIC:
if "get_weather" in validation_observer.called_functions:
    validation_observer.assert_function_called_with("get_weather", city="Tokyo")
```

**Solution**: Track validation status and ensure something is always validated:

```python
# BETTER:
weather_task_completed = False

# Validate response data
if "city" in parsed_response:
    assert parsed_response["city"].lower() == "tokyo"
    weather_task_completed = True

# Validate function calls if made
if "get_weather" in validation_observer.called_functions:
    validation_observer.assert_function_called_with("get_weather", city="Tokyo")
    weather_task_completed = True

# Ensure something was validated
assert weather_task_completed, "Weather task should be completed"
```

### 3. Print Statements Without Assertions

**Problem**: Using print statements instead of assertions:

```python
# PROBLEMATIC:
if add_calls_found:
    print(f"Found add_numbers call with args that sum to 42")
else:
    print(f"No add_numbers call with args that sum to 42 found")
```

**Solution**: Convert to proper assertions:

```python
# BETTER:
assert valid_addition_call_found, "No add_numbers call with args that sum to 42 found"
```

## Files Needing Fixes

The following files contain problematic assertions that need to be fixed:

1. `tests/integration/consolidated/test_standalone_tools.py` (Partially fixed)
2. `tests/integration/consolidated/test_class_method_tools.py`
3. `tests/integration/consolidated/test_multi_step_reasoning.py`
4. `tests/integration/consolidated/test_multi_agent.py`
5. `tests/integration/consolidated/test_validation.py`

## Implementation Steps

For each test file:

1. Identify string matching assertions (search for `in response`, `any(`, etc.)
2. Replace with proper structure validation using ValidationObserver methods
3. Find conditional assertions that might be skipped
4. Implement tracking to ensure validation happens
5. Convert print statements to proper assertions

## Testing Your Changes

After fixing each file, run the tests to ensure they still pass:

```bash
python -m pytest tests/integration/consolidated/<fixed_file>.py -v
```

If tests fail, check that your validation logic correctly handles the expected range of responses from different models. 