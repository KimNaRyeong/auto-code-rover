```python
from sympy import degree, Symbol
from sympy.abc import x

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

def test_degree_of_rational_function():
    try:
        result = degree((x-2)/(x**2+1), x)
        assert result != 1, f"Expected degree to not be 1 for a rational function, got {result}"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_degree_of_rational_function()
```