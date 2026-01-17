 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import geometry as ge, sympify
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

point1 = ge.Point(0, 0)
point2 = ge.Point(1, 1)

try:
    result = point1 + sympify(2.0) * point2
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced"

print(result)
```

When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the stack trace of the issue. The script will exit with code 0 when the issue is fixed.