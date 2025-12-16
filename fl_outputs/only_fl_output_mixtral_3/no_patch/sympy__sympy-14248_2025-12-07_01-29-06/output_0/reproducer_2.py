import sys
import traceback
from sympy import *
from sympy.matrices import MatrixSymbol

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

A = MatrixSymbol('A', 2, 2)
B = MatrixSymbol('B', 2, 2)

try:
    print("str printer:")
    print(A - A*B - B)
    print("pretty printer:")
    pprint(A - A*B - B)
    print("latex printer:")
    latex(A - A*B - B)
    assert False, "The issue was not reproduced."
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
