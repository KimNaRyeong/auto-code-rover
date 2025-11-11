Here is the reproducer script:

```python
import sympy as sp

def main():
    try:
        assert S(0.0) == S.false
        assert S(false) == S(0)
        assert S(0) == S(false)
        print("Issue not reproduced")
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
```

This script will run the assertions and if any of them fail, it will print the stack trace of the failure and then re-raise the exception.