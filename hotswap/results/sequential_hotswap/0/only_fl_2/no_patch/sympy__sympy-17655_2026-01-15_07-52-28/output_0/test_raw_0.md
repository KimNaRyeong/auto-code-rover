```python
# reproducer.py
from sympy import geometry as ge
import sympy

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

    # This works fine
    try:
        result1 = point1 + point2 * sympy.sympify(2.0)
    except Exception as e:
        print("First operation failed unexpectedly:")
        print_stacktrace(e)
        raise AssertionError("First operation should not fail") from e

    # This raises an exception
    try:
        result2 = point1 + sympy.sympify(2.0) * point2
    except Exception as e:
        print("Second operation failed as expected:")
        print_stacktrace(e)
    else:
        raise AssertionError("Second operation did not raise an error as expected")

    # If there's no exception, check results are the same (sanity check)
    if result1 != result2:
        raise AssertionError("Results should be the same but were different.")

if __name__ == "__main__":
    main()
```