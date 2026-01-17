 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

from sympy import symbols, init_printing
from sympy.physics.continuum_mechanics import Beam

init_printing()

E, I, w, l = symbols('E, I, w, l')
Ra, Ma = symbols('R_a, M_a')

b = Beam(2 * l, E, I)

b.apply_load(Ra, 