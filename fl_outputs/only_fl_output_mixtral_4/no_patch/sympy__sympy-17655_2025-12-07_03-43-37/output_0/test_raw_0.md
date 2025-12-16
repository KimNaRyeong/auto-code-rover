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
    result1 = point1 + point2 * sympify(2.0)
except Exception as e:
    print("Test 1 failed with exception:")
    print_stacktrace(e)

try:
    result2 = point1 + sympify(2.0) * point2
except Exception as e:
    print("Test 2 failed with exception:")
    print_stacktrace(e)

assert result1 == result2, "Both lines should give the same result"
```

When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the following message:

```
Test 2 failed with exception:
Traceback (most recent call last):
  File "reproducer.py", line 20
    result2 = point1 + sympify(2.0) * point2
  File "/path/to/sympy/geometry/point.py", line 222, in __add__
    raise GeometryError("Don't know how to add {} and a Point object".format(other))
GeometryError: Don't know how to add 2.0*Point2D(1, 1) and a Point object
```

This indicates that the issue is present and that both lines do not give the same result.