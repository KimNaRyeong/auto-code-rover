Here is the reproducer script:

```python
import sympy as sp

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
    try:
        p = sp.Partition([1,2])
        assert str(p) == "Partition([1, 2])"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will create a `Partition` object with the argument `[1,2]`, and then assert that its string representation is `"Partition([1, 2])"`. If the assertion fails (i.e., the actual output does not match the expected output), it will print the stack trace of the error and exit with code 1. Otherwise, it will exit with code 0.