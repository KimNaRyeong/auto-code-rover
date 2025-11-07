import sympy as sp
from sympy.physics.units import Quantity, voltage, current, ohm, convert_to

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

try:
    vs = Quantity('vs')
    vs.set_dimension(voltage)
    vs_i = Quantity('vs_i')
    vs_i.set_dimension(current)
    assert convert_to(vs/vs_i, ohm) == 'ohm', "Expected 'ohm' but got 'ohm/1000'"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
