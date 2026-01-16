```python
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

def run_pytest_tests():
    import pytest
    import os
    import sys

    # Create a temporary test file
    test_code = """
import pytest

def test_foo(caplog):
    caplog.set_level(42)

def test_bar(caplog):
    assert caplog.handler.level == 0, f"Expected log level 0, got {caplog.handler.level}"
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(directory, "temp_test_logging.py")
    with open(test_file_path, "w") as test_file:
        test_file.write(test_code)
    
    # Run pytest and capture the output
    test_result = pytest.main([test_file_path, "-qq"])
    
    # Clean up
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    # Check test result
    if test_result != 0:
        raise AssertionError("caplog fixture does not restore log level after test.")

def main():
    try:
        run_pytest_tests()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issue found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```
This script `reproducer.py` dynamically creates a temporary test file to simulate the issue described with the caplog fixture in pytest. It asserts that after modifying the log level in one test, the level should be reset to its default for the next test. If the issue is present, it will raise an `AssertionError` and print a detailed stack trace. If not, it will exit with code 0, indicating the absence of the issue.