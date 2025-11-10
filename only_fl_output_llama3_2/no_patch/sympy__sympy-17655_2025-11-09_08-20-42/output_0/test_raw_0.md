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
        raise AssertionError("Issue present")

    if not isinstance(result1, ge.Point) or not isinstance(result2, ge.Point):
        print_stacktrace(Exception("Unexpected type"))
        raise AssertionError("Issue present")

    if result1 != result2:
        print_stacktrace(Exception("Unexpected result"))
        raise AssertionError("Issue present")

    print("Issue fixed")

if __name__ == "__main__":
    main()
```

This script will run the two lines of code that reproduce the issue, and then check if the results are equal. If the issue is present (i.e., an exception is raised or the results are not equal), it will print a stack trace and raise an `AssertionError`.