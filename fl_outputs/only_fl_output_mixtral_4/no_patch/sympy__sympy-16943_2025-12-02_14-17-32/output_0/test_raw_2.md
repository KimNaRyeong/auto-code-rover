 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
    assert type(p) is not list, "fps() did not return a list for a polynomial input"
    try:
        p[0]
    except TypeError as e:
        print_stacktrace(e)
        assert False, "fps() returned a non-indexable object for a polynomial input"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will exit with code 0.