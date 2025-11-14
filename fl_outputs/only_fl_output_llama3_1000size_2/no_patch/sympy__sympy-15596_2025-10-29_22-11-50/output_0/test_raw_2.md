Here is the reproducer script:

```python
import sympy as sp

def reproduce_issue():
    try:
        f = sp.symbols('x')
        result = sp.degree((f-2)/(f**2+1), f)
        assert result == 2, "Expected degree of rational function to be 2"
    except Exception as e:
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
    reproduce_issue()
```

This script will attempt to compute the degree of a rational function using SymPy. If the issue is present and the degree is not computed correctly, it will print the stack trace and raise an `AssertionError`.