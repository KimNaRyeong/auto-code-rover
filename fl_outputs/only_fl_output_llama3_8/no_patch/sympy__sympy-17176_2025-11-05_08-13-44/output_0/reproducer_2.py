import sympy as sp
from sympy import symbols, Xor
from sympy.logic.boolalg import _finger
from pprint import pprint
import traceback
import sys
from collections import defaultdict

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

def reproduce_issue():
    try:
        A1, A2, A3 = symbols('A1,A2,A3')
        f1 = Xor(A1, A2, A3)
        f2 = ~Xor(A1, A2, A3)
        bool_map_output = sp.bool_map(f1, f2)
        if str(bool_map_output) != "((A1 & A2 & A3) | (A1 & ~A2 & ~A3) | (A2 & ~A1 & ~A3) | (A3 & ~A1 & ~A2), {A1: A1, A2: A2, A3: A3})":
            raise AssertionError("Expected bool_map output does not match the actual output")
        
        a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
        b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
        if str(a) != "defaultdict(<class 'list'>, {(0, 0, 2, 2, 8): [A1, A2, A3]})" or str(b) != "defaultdict(<class 'list'>, {(0, 0, 2, 2, 8): [A1, A2, A3]})":
            raise AssertionError("Expected fingerprint does not match the actual fingerprint")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
