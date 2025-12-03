 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import sympy as sp

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

def test_extract_multiplicatively():
    x, y = sp.symbols('x y')
    a = -2*x - 4*y - 8
    b = -2 - 4*sp.I
    c = 2 + 4*sp.I
    d = -2*x - 2*y

    assert a.extract_multiplicatively(-2) == -x - 2*y - 4
    assert b.extract_multiplicatively(-1) == c
    assert c.extract_multiplicatively(2) == 1 + 2*sp.I
    assert d.extract_multiplicatively(-2) == -2*x - 2*y
    assert d.extract_multiplicatively(-1) == 2*x + 4*y + 8
    assert a.extract_multiplicatively(-1) == 2*x + 4*y + 8
    assert a.extract_multiplicatively(-2) is None  # this should raise AssertionError

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` with a stack trace, indicating that the issue is present.