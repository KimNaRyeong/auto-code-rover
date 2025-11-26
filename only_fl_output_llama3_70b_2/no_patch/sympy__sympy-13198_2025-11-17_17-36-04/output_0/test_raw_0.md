Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy import Symbol, Matrix, lambdify

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

q_1, q_2, q_3 = sp.symbols('q_1 q_2 q_3')
Mq = Matrix([
    [(sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.sin(q_1)**2 + (sp.cos(q_2) + 0.5*sp.cos(q_2 + q_3))**2*sp.cos(q_1)**2 + 0.25*sp.sin(q_1)**2*sp.cos(q_2)**2 + 0.25*sp.cos(q_1)**2*sp.cos(q_2)**2, 0, 0],
    [0, (-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.sin(q_1)**2 + (-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))**2*sp.cos(q_1)**2 + (-sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))**2 + 0.25*sp.sin(q_1)**2*sp.sin(q_2)**2 + 0.25*sp.sin(q_2)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2)**2, -0.5*(-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3)],
    [0, -0.5*(-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_1)**2*sp.sin(q_2 + q_3) - 0.5*(-sp.sin(q_2) - 0.5*sp.sin(q_2 + q_3))*sp.sin(q_2 + q_3)*sp.cos(q_1)**2 - 0.5*(-sp.cos(q_2) - 0.5*sp.cos(q_2 + q_3))*sp.cos(q_2 + q_3), 0.25*sp.sin(q_1)**2*sp.sin(q_2 + q_3)**2 + 0.25*sp.sin(q_2 + q_3)**2*sp.cos(q_1)**2 + 0.25*sp.cos(q_2 + q_3)**2]
])

Mqs = sp.simplify(Mq)
Mqs_fnc = lambdify((q_1, q_2, q_3), Mqs)

try:
    result = Mqs_fnc(0, 0, 0)
    assert (result == [[2.5, 0., 0.], [0., 2.5, 0.75], [0., 0.75, 0.25]]).all(), "Simplification result is incorrect"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.