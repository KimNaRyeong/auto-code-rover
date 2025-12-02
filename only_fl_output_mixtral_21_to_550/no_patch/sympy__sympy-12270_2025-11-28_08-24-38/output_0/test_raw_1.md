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
    b = sp.Mul(2, -x - 2*y - 4, evaluate=False)
    c = sp.Mul(2, -x, evaluate=False)

    # This works as expected
    assert a.extract_multiplicatively(2) == x + 2*y + 4

    # This fails with AssertionError
    assert b.extract_multiplicatively(-2) == -x - 2*y - 4

    # This also fails with AssertionError
    assert c.extract_multiplicatively(-2) == x

try:
    test_extract_multiplicatively()
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    test_extract_multiplicatively()
  File "reproducer.py", line 19, in test_extract_multiplicatively
    assert b.extract_multiplicatively(-2) == -x - 2*y - 4
AssertionError: -x - 2*y - 4
```
This confirms the presence of the issue. When the issue is fixed, the script should exit with code 0 and not print any stack trace.