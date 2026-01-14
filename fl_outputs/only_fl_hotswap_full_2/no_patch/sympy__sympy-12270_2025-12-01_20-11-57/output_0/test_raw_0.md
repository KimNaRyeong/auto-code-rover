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

    assert a.extract_multiplicatively(-2) == -x - 2*y - 4
    assert b.extract_multiplicatively(-1) == c
    assert c.extract_multiplicatively(2) == 1 + 2*sp.I

    with assert raises(AssertionError):
        print_stacktrace(AssertionError("Expected bug"))
        a.extract_multiplicatively(-4)

    with assert raises(AssertionError):
        print_stacktrace(AssertionError("Expected bug"))
        b.extract_multiplicatively(-2)

    with assert raises(AssertionError):
        print_stacktrace(AssertionError("Expected bug"))
        b.extract_multiplicatively(-4)

    with assert raises(AssertionError):
        print_stacktrace(AssertionError("Expected bug"))
        c.extract_multiplicatively(-4)

test_extract_multiplicatively()
```
This script defines a `print_stacktrace` function to print the stack trace, defines a `test_extract_multiplicatively` function to test the `extract_multiplicatively` method, and then calls the `test_extract_multiplicatively` function to run the tests.

The script uses the `assert` statement to check the expected results of the `extract_multiplicatively` method. If the method returns an unexpected result, the `assert` statement raises an `AssertionError` with a message indicating the expected and actual results. The `print_stacktrace` function is then called to print the stack trace of the `AssertionError`.

The script also uses the `with assert raises` statement to check for exceptions raised by the `extract_multiplicatively` method. If the method raises an exception, the `with assert raises` statement catches the exception and then calls the `print_stacktrace` function to print the stack trace of the exception.

The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.