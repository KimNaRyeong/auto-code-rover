 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import sympy as sp
from sympy.abc import q_1, q_2, q_3

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    q = [q_1, q_2, q_3]

    Mq = sp.Matrix([
        [
            (sp.cos(q_2) + 0.5 * sp.cos(q_2 + q_3))**2 * sp.sin(q_1)**2 +
            (sp.cos(q_2) + 0.5 * sp.cos(q_2 + q_3))**2 * sp.cos(q_1)**2 +
            0.25 * sp.sin(q_1)**2 * sp.cos(q_2)**2 +
            0.25 * sp.cos(q_1)**2 * sp.cos(q_2)**2,
            0,
            0,
        ],
        [
            0,
            (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3))**2 * sp.sin(q_1)**2 +
            (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3))**2 * sp.cos(q_1)**2 +
            (-sp.cos(q_2) - 0.5 * sp.cos(q_2 + q_3))**2 +
            0.25 * sp.sin(q_1)**2 * sp.sin(q_2)**2 +
            0.25 * sp.sin(q_2)**2 * sp.cos(q_1)**2 +
            0.25 * sp.cos(q_2)**2,
            -0.5 * (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3)) * sp.sin(q_1)**2 * sp.sin(q_2 + q_3) -
            0.5 * (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3)) * sp.sin(q_2 + q_3) * sp.cos(q_1)**2 -
            0.5 * (-sp.cos(q_2) - 0.5 * sp.cos(q_2 + q_3)) * sp.cos(q_2 + q_3),
        ],
        [
            0,
            -0.5 * (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3)) * sp.sin(q_1)**2 * sp.sin(q_2 + q_3) -
            0.5 * (-sp.sin(q_2) - 0.5 * sp.sin(q_2 + q_3)) * sp.sin(q_2 + q_3) * sp.cos(q_1)**2 -
            0.5 * (-sp.cos(q_2) - 0.5 * sp.cos(q_2 + q_3)) * sp.cos(q_2 + q_3),
            0.25 * sp.sin(q_1)**2 * sp.sin(q_2 + q_3)**2 +
            0.25 * sp.sin(q_2 + q_3)**2 * sp.cos(q_1)**2 +
            0.25 * sp.cos(q_2 + q_3)**2,
        ],
    ])

    Mq_fnc = sp.lambdify(q, Mq