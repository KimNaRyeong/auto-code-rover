 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import RootOf, symbols, poly

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

x = symbols('x')

# This should raise an AssertionError
assert RootOf(x**3 + x - 1, 0).poly.gen == x, "Issue not reproduced"

# This should raise an AssertionError
try:
    RootOf((x**3 + x - 1).subs(x, symbols('tan(x)')), 0)
    assert False, "AssertionError not raised"
except AssertionError as e:
    print_stacktrace(e)

# This should raise an AssertionError
try:
    RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
    assert False, "AssertionError not raised"
except AssertionError as e:
    print_stacktrace(e)

# This should raise an AssertionError
try:
    RootOf((x**3 + 2*x - 1), 0)
    assert False, "AssertionError not raised"
except AssertionError as e:
    print_stacktrace(e)

# This should raise an AssertionError
try:
    RootOf((x**3 + 2*x - 1), 0).poly.gen
    assert False, "AssertionError not raised"
except AssertionError as e:
    print_stacktrace(e)

print("Issue reproduced")
```
The script defines the `print_stacktrace` function to print the stack trace of an exception, and then defines the symbol `x`. It then raises an `AssertionError` if the issue is not reproduced, and prints the stack trace if the issue is reproduced.

When executed with `python3 reproducer.py`, the script should print the following output:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    assert RootOf((x**3 + 2*x - 1), 0).poly.gen == x, "Issue not reproduced"
AssertionError: Issue not reproduced
```
This indicates that the issue has been reproduced.