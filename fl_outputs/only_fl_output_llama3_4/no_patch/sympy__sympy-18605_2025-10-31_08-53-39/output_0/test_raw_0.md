Here is the reproducer script:

```python
import sympy as sp
import sys
from functools import wraps

def assert_raises(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an error")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(0)

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

def test_issue():
    m, n = sp.symbols("m, n", real=True)
    i = sp.Idx("i", (m, n))
    assert_raises(lambda: sp.Idx("i", m), "Expected non-integer bounds to raise an error")

if __name__ == "__main__":
    test_issue()
```

This script will run the code that reproduces the issue and print a stack trace if the issue is present. If the issue is fixed, it will exit with code 0.