import sympy as sp
from sympy.physics.units import convert_to
from sympy.physics.units.systems.si import joule, second, kilogram, meter

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

joule = joule
second = second
kg = kilogram
m = meter
s = 1/second

J = kg*m**2/s**2

try:
    result = convert_to(J*second, joule)
    assert result == J*second or result == kg*m**2/s, f"Expected J*s or kg*m**2/s, but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present. Exiting with code 0.")
exit(0)
