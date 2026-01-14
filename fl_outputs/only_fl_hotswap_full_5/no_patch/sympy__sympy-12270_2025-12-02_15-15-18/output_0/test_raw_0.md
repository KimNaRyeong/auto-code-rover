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

    assert sp.extract_multiplicatively(-2, a) == -x - 2*y - 4
    assert sp.extract_multiplicatively(-2, b) == 1
    assert sp.extract_multiplicatively(-2, c) == None
    assert sp.extract_multiplicatively(-2, a*c) == -2*(x + 2*y + 4)*(1 + 2*sp.I)

    with assertion_error():
        sp.extract_multiplicatively(-2, a*a)

try:
    test_extract_multiplicatively()
except AssertionError as e:
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating the presence of the issue. The script will exit with code 1.

When the issue is fixed, the script will exit with code 0, indicating no errors.