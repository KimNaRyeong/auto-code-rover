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
        raise AssertionError("Issue not fixed")

    if result1 != result2:
        print_stacktrace(Exception("Expected behavior not met"))
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script will run the two expressions and compare their results. If they are different, it will print a stack trace of the issue and exit with code 1.