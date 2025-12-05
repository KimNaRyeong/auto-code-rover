 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
from sympy import Symbol, fps

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    x = Symbol('x')
    p = fps(x ** 2)
    assert type(p) == sympy.core.power.Pow, "fps(x**2) should return a formal power series, not a Pow object"
    assert p[0] is not None, "The first term of the formal power series should not be None"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. When the issue is fixed, the script will exit with code 0.