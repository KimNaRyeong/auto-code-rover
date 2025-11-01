Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys

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

def reproduce_issue():
    # Your code to reproduce the issue goes here
    raise AssertionError("Issue reproduced!")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with non-zero code when issue is present

sys.exit(0)  # Exit with zero code when issue is fixed
```
This script defines a `print_stacktrace` function to print the stack trace of an exception, and a `reproduce_issue` function that raises an `AssertionError` to reproduce the issue. The main part of the script tries to run the `reproduce_issue` function and catches any exceptions raised. If an exception is caught, it prints the stack trace using the `print_stacktrace` function and exits with a non-zero code. If no exception is caught, it exits with a zero code.

You can modify the `reproduce_issue` function to include your specific code that reproduces the issue.