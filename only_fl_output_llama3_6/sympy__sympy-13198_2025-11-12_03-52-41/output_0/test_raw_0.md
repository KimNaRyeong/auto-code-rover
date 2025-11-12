Here is the reproducer script:

```python
import sympy as sp
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
    x, y = sp.symbols('x y')
    z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
    w = sp.expand(z)
    v = sp.factor(w)

    if not sp.simplify(v) == sp.sympify('1.0e-8*x**2 + 5.0e-8*x*y + 4.0e-8*y**2'):
        raise AssertionError("Issue present")

    q_1, q_2, q_3 = sp.symbols('q_1 q_2 q_3')
    q = [q_1,q_2,q_3]

    Mq = sp.Matrix([[(1.0*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.sin(q_1)**2 + (1.0*sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.cos(q_1)**2 + 0.25*sp.sin(q_1)**2*sp.cos(q_2)**2 + 0.25*sp.cos(q_1)**2*sp.cos(q_2)**2, 0, 0], [0, (-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.sin(q_1)**2 + (-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.cos(q_1)**2 + (-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))**2 + 0.25*sp.sin(q_1)**2*sp.sin(q_2)**2 + 0.25*sp.sin(q_2)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2)**2, -0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3)], [0, -0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-1.0*sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-1.0*sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3), 0.25*sp.sin(q_1)**2*sp.sin(q_2 + q_3)**2 + 0.25*sp.sin(q_2 + q_3)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2 + q_3)**2]])

    Mqs = sp.simplify(Mq)
    if not Mqs.subs({q_1: 0, q_2: 0, q_3: 0}) == sp.Matrix([[ 2.5, 0, 0], [0, 2.5, 0.75], [0, 0.75, 0.25]]):
        raise AssertionError("Issue present")

    if not Mqs.subs({q_1: 0}).equals(Mq.subs({q_1