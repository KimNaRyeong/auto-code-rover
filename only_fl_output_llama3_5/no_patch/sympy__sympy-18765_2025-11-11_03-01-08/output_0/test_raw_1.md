Here is the reproducer script:

```python
import sympy as sp
from sympy import Add, MatAdd, Symbol, MatrixSymbol

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
    x = Symbol('x')
    assert Add(x, x, evaluate=True) == 2*x
    A = MatrixSymbol('A', 2, 2)
    if MatAdd(A, A).func != Add:
        raise AssertionError("MatAdd and MatMul are behaving differently from Add and Mul.")
    try:
        assert MatAdd(A, A, evaluate=True) == 2*A
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function when executed with `python3 reproducer.py`. The function first checks if adding a symbolic variable to itself using `Add` evaluates correctly. Then, it defines a 2x2 matrix symbol and adds it to itself using `MatAdd`. If this does not evaluate correctly, an AssertionError is raised.