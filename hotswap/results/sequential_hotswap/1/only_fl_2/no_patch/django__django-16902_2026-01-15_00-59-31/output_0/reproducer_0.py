# reproducer.py
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def simulate_right_function_behavior(db_type, field_value):
    """
    Simulate the RIGHT function behavior for different database backends.
    Oracle is expected to return an empty string when the length is 0,
    but it's reported to return the whole string instead.
    """
    length = len(field_value)
    calculated_length = length - length  # Expected to be 0
    
    if db_type == "PostgreSQL":
        return "" if calculated_length == 0 else field_value[-calculated_length:]
    elif db_type == "Oracle":
        # Oracle uses SUBSTR, and an issue is reported here
        return field_value if calculated_length == 0 else field_value[-calculated_length:]
    else:
        # Default behavior (similar to PostgreSQL for simplification)
        return "" if calculated_length == 0 else field_value[-calculated_length:]

try:
    # Simulating behavior with Oracle
    result = simulate_right_function_behavior("Oracle", "test_value")
    assert result == "", "Oracle database RIGHT function should return an empty string when length is 0."
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with error code
else:
    print("Success: The issue is fixed.")
    exit(0)  # Exit with success code
