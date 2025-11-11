Here is the reproducer script:

```python
import sympy
from sympy import geometry as ge

def main():
    point1 = ge.Point(0, 0)
    point2 = ge.Point(1, 1)

    try:
        result1 = point1 + point2 * sympy.sympify(2.0)
        result2 = point1 + sympy.sympify(2.0) * point2
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected both lines to work without raising an exception")

    if not isinstance(result1, ge.Point) or not isinstance(result2, ge.Point):
        print_stacktrace(Exception("Result is not a Point object"))
        raise AssertionError("Expected both results to be Point objects")

    if result1 != result2:
        print_stacktrace(Exception("Results are different"))
        raise AssertionError("Expected both lines to give the same result")

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by executing both lines of code and checking that they do not raise an exception. It also checks that the results are the same, and if either check fails, it prints a stack trace and raises an `AssertionError`.