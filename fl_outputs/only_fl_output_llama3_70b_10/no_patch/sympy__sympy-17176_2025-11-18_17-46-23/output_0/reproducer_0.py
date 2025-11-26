from sympy import *
from sympy.logic.boolalg import _finger
from pprint import pprint

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
    A1,A2,A3 = symbols('A1,A2,A3')
    f1 = Xor(A1,A2,A3)
    f2 = ~(Xor(A1,A2,A3))
    bool_map_result = bool_map(f1, f2)
    expected_result = (~(A1 & A2 & A3) & ((A1 | A2 | A3) ^ (A1 & A2 & A3)))
    assert bool_map_result == expected_result, "bool_map result is incorrect"

    a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
    b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
    assert a != b, "_finger fingerprint is incorrect"

    print("Issue not present. Exiting with code 0.")
    exit(0)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
