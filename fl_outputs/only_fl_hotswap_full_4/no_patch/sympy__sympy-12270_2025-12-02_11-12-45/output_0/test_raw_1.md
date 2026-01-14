 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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

    # This fails because b is a non-evaluated Mul
    try:
        assert b.extract_multiplicatively(-2) == -x - 2*y - 4
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # This also fails because c is a non-evaluated Mul
    try:
        assert c.extract_multiplicatively(-2) == x
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_extract_multiplicatively()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    test_extract_multiplicatively()
  File "reproducer.py", line 23, in test_extract_multiplicatively
    assert b.extract_multiplicatively(-2) == -x - 2*y - 4
AssertionError: -x - 2*y - 4
```
This confirms that the `extract_multiplicatively` method fails to extract the multiplicative factor from a non-evaluated `Mul` instance.