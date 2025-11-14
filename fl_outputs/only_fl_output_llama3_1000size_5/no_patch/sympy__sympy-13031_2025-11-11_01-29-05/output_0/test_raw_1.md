Here is the reproducer script:

```python
import sympy as sy

def reproduce_issue():
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)

    expected_shape = (0, 6)
    actual_shape = sy.Matrix.hstack(M1, M2, M3, M4).shape

    if actual_shape != expected_shape:
        print("Expected shape: {0}, Actual shape: {1}".format(expected_shape, actual_shape))
        raise AssertionError("Matrix hstack behavior changed in sympy 1.1")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script creates matrices with different shapes and checks if the expected shape is returned by `sy.Matrix.hstack`. If the actual shape does not match the expected shape, it prints an error message and raises an `AssertionError` with a stack trace.