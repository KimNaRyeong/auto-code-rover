 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *
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

def main():
    init_printing()
    x = symbols('x')
    A = Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    B = exp(A)
    C = simplify(B)
    D = C.applyfunc(lambda f: sin(f))
    E = C.applyfunc(lambda f: cos(f))
    F = C.applyfunc(lambda f: -sin(f))
    G = Matrix([[D[0,0]], [E[0,0]], [F[0,0]]])
    H = Matrix([[C[0,0]], [C[1,0]], [C[2,0]]])
    I = Matrix([[C[0,1]], [C[1,1]], [C[2,1]]])
    J = Matrix([[C[0,2]], [C[1,2]], [C[2,2]]])
    K = Matrix([[G[0,0]], [E[0,0]], [F[0,0]]])
    L = Matrix([[C[0,0]], [C[1,0]], [C[2,0]]])
    M = Matrix([[C[0,1]], [C[1,1]], [C[2,1]]])
    N = Matrix([[C[0,2]], [C[1,2]], [C[2,2]]])
    assert (K == sin(L)).all(), "AssertionError: sin(1) has not been recognized"
    print("Test passed!")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(2)
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.