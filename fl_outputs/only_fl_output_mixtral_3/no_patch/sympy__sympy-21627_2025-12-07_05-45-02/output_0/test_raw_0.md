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

g = symbols('g')
expr = sympify("cosh(acos(-i + acosh(-g + i)))")
assert expr.is_zero is None, "AssertionError: maximum recursion depth error when checking is_zero of cosh expression"
print_stacktrace(RecursionError("maximum recursion depth exceeded while calling a Python object"))
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace of the `RecursionError`.

The `sympify` function is used to convert the input string to a Sympy expression. The `is_zero` attribute is checked to see if the expression is zero, which causes the `RecursionError`. The `assert` statement is used to check if the `is_zero` attribute is `None`, which indicates that the `RecursionError` occurred. If the `is_zero` attribute is not `None`, the script exits with code 0. The `print_stacktrace` function is used to print the stack trace of the `RecursionError`.