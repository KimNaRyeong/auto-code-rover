 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from sympy import sympify, ceiling, simplify

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    x = ceiling(sympify('x/4 - 3/4', evaluate=False))
    y = 4 * x
    z = simplify(y)

    if z != 4 * ceiling(sympify('x/4 - 3/4', evaluate=False)):
        raise AssertionError("Behavior is inconsistent")

if __name__ == "__main__":
    try:
        reproduce_issue()
        print("Issue is fixed")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
The script defines a function `reproduce_issue()` that performs the same steps as in the issue description. If the behavior is inconsistent, it raises an `AssertionError`. The `print_stacktrace()` function is used to print the stack trace when the error is raised.

To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will print "Issue is fixed" and exit with code 0.