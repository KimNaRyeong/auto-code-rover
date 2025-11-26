import sys
from sympy import symbols, init_printing
from sympy.physics.continuum_mechanics import Beam

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

init_printing()

E, I, w, l = symbols('E, I, w, l')
Ra, Ma = symbols('R_a, M_a')

b = Beam(2 * l, E, I)

b.apply_load(Ra, 0, -1)
b.apply_load(-Ma, 0, -2)
b.apply_load(-w * l, l, -1)
b.apply_load(-w / l, l, 1)
b.apply_load(-w * l**2 / 2, 2 * l, -2)

expected_output = "BeamLoad(R_a, 0, -1)\nBeamLoad(-M_a, 0, -2)\nBeamLoad(-w*l, l, -1)\nBeamLoad(-w/l, l, 1)\nBeamLoad(-w*l**2/2, 2*l, -2)"
try:
    assert str(b.load) == expected_output
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
