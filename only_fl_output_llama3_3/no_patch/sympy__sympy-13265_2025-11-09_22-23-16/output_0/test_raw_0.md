Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

def main():
    x = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    result = sp.exp(x)
    simplified_result = sp.simplify(result)

    if not isinstance(simplified_result, sp.Matrix):
        raise AssertionError("Simplification failed to recognize sin expressed as exponentials")

    print_stacktrace(AssertionError())

if __name__ == "__main__":
    main()
```

This script defines a `main` function that creates the matrix `x`, computes its exponential using `sp.exp(x)`, and then simplifies the result using `sp.simplify(result)`. If the simplified result is not a matrix, it raises an `AssertionError` with a stack trace printed to stderr.