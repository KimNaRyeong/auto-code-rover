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

    if str(z) != '4*ceiling(x/4) - 3':
        raise AssertionError(f'Inconsistent behavior for sympify/simplify with ceiling: {z}')

if __name__ == '__main__':
    try:
        reproduce_issue()
        print('Issue not found.')
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, the script will print 'Issue not found.' and exit with code 0.