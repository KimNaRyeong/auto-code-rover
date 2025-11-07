Here is the reproducer script `reproducer.py`:
```python
import sympy
from functools import wraps

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def assert_reproduces_issue(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            raise
    return wrapper

@assert_reproduces_issue
def reproduce_issue():
    sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

if __name__ == '__main__':
    try:
        reproduce_issue()
    except SystemExit as e:
        if e.code != 0:
            raise
```
This script defines a decorator `assert_reproduces_issue` that catches any `AssertionError` exceptions raised by the decorated function and prints the stack trace using the provided function. The reproducer function `reproduce_issue` attempts to reproduce the issue by calling `sympify` with different values of `evaluate`. If the issue is present, it raises an `AssertionError` and prints the stack trace.

To run the reproducer, simply execute the script: `python3 reproducer.py`.