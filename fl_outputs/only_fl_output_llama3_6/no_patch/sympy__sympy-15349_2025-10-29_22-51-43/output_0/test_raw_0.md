Here is the reproducer script:

```python
import sympy
from sympy import symbols, Quaternion
import traceback
import sys

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

def reproduce_issue():
    try:
        x = symbols('x')
        q = Quaternion(sympy.cos(x/2), sympy.sin(x/2), 0, 0)
        result = trigsimp(q.to_rotation_matrix())
        if not all([result[i][1] < 0 for i in range(3)]):
            raise AssertionError("Incorrect result")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script can be run with `python3 reproducer.py`. If the issue is present, it will print a stack trace and exit with code 1.