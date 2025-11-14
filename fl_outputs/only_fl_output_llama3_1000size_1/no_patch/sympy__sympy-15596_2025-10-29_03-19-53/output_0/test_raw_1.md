Here is the reproducer script:

```python
import sympy as sp
from io import StringIO
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        result = sp.degree((sp.Symbol('x') - 2) / ((sp.Symbol('x'))**2 + 1), sp.Symbol('x'))
        assert_that(result).is_equal_to(1)
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will attempt to compute the degree of a rational function using SymPy, and if it fails, it will print the stack trace and raise an `AssertionError`.