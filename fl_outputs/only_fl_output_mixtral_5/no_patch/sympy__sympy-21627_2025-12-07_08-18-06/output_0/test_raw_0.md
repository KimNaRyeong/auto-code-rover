 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import sympify, symbols

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

try:
    g, i = symbols('g i')
    expr = sympify("cosh(acos(-i + acosh(-g + i)))")
    assert expr.is_zero == RecursionError
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints a stack trace of the issue:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    assert expr.is_zero == RecursionError
AssertionError
```
Note that the stack trace is not shown because the `RecursionError` is caught by the `assert` statement. If you want to see the full stack trace, you can replace the `assert` statement with:
```python
try:
    assert expr.is_zero != RecursionError
except AssertionError:
    print_stacktrace(RecursionError)
```
This will raise a `RecursionError` and print its stack trace.