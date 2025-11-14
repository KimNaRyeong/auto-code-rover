import sympy as sp
from pprint import pprint
from traceback import extract_tb
import sys

def print_stacktrace(e: Exception):
    tb = extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

A1, A2, A3 = sp.symbols('A1,A2,A3')
f1 = sp.Xor(A1, A2, A3)
f2 = ~(sp.Xor(A1, A2, A3))
bool_map_result = sp.bool_map(f1, f2)

expected_result = ((A1 & A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3) | (~A1 & ~A2 & ~A3), {A1: A1, A2: A2, A3: A3})

try:
    assert bool_map_result == expected_result
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

from sympy.logic.boolalg import _finger

a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))

try:
    assert a != b
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not present. Exiting with code 0.")
sys.exit(0)
