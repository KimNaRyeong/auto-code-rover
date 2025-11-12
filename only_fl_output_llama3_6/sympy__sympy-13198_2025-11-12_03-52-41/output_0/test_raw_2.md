Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy.abc import x, y, z
import traceback
import sys

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
    q_1 = sp.Symbol('q_1')
    q_2 = sp.Symbol('q_2')
    q_3 = sp.Symbol('q_3')
    q = [q_1, q_2, q_3]

    Mq = sp.Matrix([
        [(1.0*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.sin(q_1)**2 +
         (1.0*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.cos(q_1)**2 +
         0.25*sp.sin(q_1)**2*sp.cos(q_2)**2 +
         0.25*sp.cos(q_1)**2*sp.cos(q_2)**2, 0, 0],
        [0, (-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.sin(q_1)**2 +
         (-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.cos(q_1)**2 +
         (-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))**2 +
         0.25*sp.sin(q_1)**2*sp.sin(q_2)**2 +
         0.25*sp.sin(q_2)**2*sp.cos(q_1)**2 +
         0.25*sp.cos(q_2)**2, -0.5*(-1.0*sp.sin(q_2) -
         0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) -
         0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*
         sp.sin(q_2 + q_3)*sp.cos(q_1)**2 -
         0.5*(-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3)],
        [0, -0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*
         sp.sin(q_1)**2*sp.sin(q_2 + q_3) -
         0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*
         sp.sin(q_2 + q_3)*sp.cos(q_1)**2 -
         0.5*(-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3),
         0.25*sp.sin(q_1)**2*sp.sin(q_2 + q_3)**2 +
         0.25*sp.sin(q_2 + q_3)**2*sp.cos(q_1)**2 +
         0.25*sp.cos(q_2 + q_3)**2]
    ])

    try:
        Mqs = sp.simplify(Mq)
        Mqs_fnc = sp.lambdify(q, Mqs)
        assert round(Mqs_fnc(0, 0, 0)[0][0], 8) == 2.5
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.