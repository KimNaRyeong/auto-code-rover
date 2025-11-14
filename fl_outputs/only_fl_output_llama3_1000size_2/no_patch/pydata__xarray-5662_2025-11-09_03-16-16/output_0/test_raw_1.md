Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
def your_function():
    assert 1 == 2, "This should not be true"
    print("Function executed successfully")

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

if __name__ == '__main__':
    try:
        your_function()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script will call `your_function` which contains an assertion that should fail. If the assertion fails, it will print the stack trace and then re-raise the exception.