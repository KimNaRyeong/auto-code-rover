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
        if result != 1:
            raise AssertionError("Expected degree of rational function to be 1, but got {}".format(result))
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will attempt to compute the degree of a rational function using SymPy. If the result is not equal to 1, it will raise an `AssertionError` and print the stack trace.