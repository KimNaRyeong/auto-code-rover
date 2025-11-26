from sympy import *
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

try:
    A1, A2 = symbols('A1,A2')
    f1 = Xor(A1,A2)
    f2 = ~Xor(A1,A2)

    map_f2_f1 = bool_map(f2,f1)
    map_f1_f2 = bool_map(f1,f2)

    assert not (str(map_f2_f1) == str(((A1 & A2) | (~A1 & ~A2)), {}) and (str(map_f1_f2) == str(((A1 & ~A2) | (A2 & ~A1)), {})), "bool_map returned an incorrect symbol mapping"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue is fixed!")
sys.exit(0)
