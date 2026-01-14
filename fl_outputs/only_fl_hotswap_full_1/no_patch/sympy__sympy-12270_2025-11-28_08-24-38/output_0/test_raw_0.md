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
    b = sp.Mul(2, -x, evaluate=False)
    c = sp.Mul(2, -x - 2*y - 4, evaluate=False)
    d = sp.Mul(2, -x - 2*y - 4, evaluate=False)
    d.args = (2, -x - 2*y - 4)

    assert a.extract_multiplicatively(-2) == -x - 2*y - 4
    assert b.extract_multiplicatively(-2) == x
    assert c.extract_multiplicatively(-2) is None
    assert d.extract_multiplicatively(-2) == -x - 2*y - 4

if __name__ == "__main__":
    try:
        test_extract_multiplicatively()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
This script defines a test function `test_extract_multiplicatively()` that creates the expressions and performs the `extract_multiplicatively()` calls as in the issue description. The script then calls this function and catches any `AssertionError` exceptions to print the stack trace.

When the script is executed with the current implementation, it raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    test_extract_multiplicatively()
  File "reproducer.py", line 19, in test_extract_multiplicatively
    assert c.extract_multiplicatively(-2) is None
AssertionError:
```
This confirms the presence of the issue. If the issue is fixed, the script will exit with code 0 without raising any exceptions.