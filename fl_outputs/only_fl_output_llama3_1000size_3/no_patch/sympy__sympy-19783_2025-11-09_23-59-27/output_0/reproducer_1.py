import sympy as sp
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
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
        from sympy.physics.quantum.dagger import Dagger
        from sympy.physics.quantum.operator import Operator
        from sympy.physics.quantum import IdentityOperator
        A = Operator('A')
        Identity = IdentityOperator()
        assert A * Identity == A, "Dagger() * IdentityOperator() is not simplified"
        B = Dagger(A)
        result = str(B * Identity)
        if result != "A.dagger":
            raise AssertionError("Dagger() * IdentityOperator() is not simplified")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
