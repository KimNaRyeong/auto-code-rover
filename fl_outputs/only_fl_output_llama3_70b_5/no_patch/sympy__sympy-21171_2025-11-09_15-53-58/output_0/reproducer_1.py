import sympy as sp
from sympy.physics.continuum_mechanics import Beam
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproducer():
    # Young's modulus
    E = sp.symbols("E")
    # length of the beam
    L = sp.symbols("L")
    # concentrated load at the end tip of the beam
    F = sp.symbols("F")
    # square cross section
    B, H = sp.symbols("B, H")
    I = B * H**3 / 12
    # numerical values (material: steel)
    d = {B: 1e-02, H: 1e-02, E: 210e09, L: 0.2, F: 100}

    b2 = Beam(L, E, I)
    b2.apply_load(-F, L / 2, -1)
    b2.apply_support(0, "fixed")
    R0, M0 = sp.symbols("R_0, M_0")
    b2.solve_for_reaction_loads(R0, M0)

    try:
        sf_latex = sp.latex(b2.shear_force())
        print(sf_latex)  # This should raise a TypeError
    except TypeError as e:
        print_stacktrace(e)
        assert False, "TypeError raised"

if __name__ == "__main__":
    reproducer()
