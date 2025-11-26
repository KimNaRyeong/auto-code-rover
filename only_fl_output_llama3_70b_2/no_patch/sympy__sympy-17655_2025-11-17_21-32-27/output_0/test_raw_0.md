Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import sympy
from sympy import geometry as ge

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

def main():
    point1 = ge.Point(0, 0)
    point2 = ge.Point(1, 1)

    try:
        result1 = point1 + point2 * sympy.sympify(2.0)
        result2 = point1 + sympy.sympify(2.0) * point2
        assert result1 == result2, "Expected same results for both expressions"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    main()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.