from sympy.physics.quantum.dagger import Dagger
from sympy.physics.quantum.operator import Operator
from sympy.physics.quantum import IdentityOperator

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

def test_dagger_identity_product():
    A = Operator('A')
    Identity = IdentityOperator()
    B = Dagger(A)

    assert A * Identity == A, "A * Identity should simplify to A"
    try:
        assert B * Identity == B, "B * Identity should simplify to B"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error status
    else:
        print("All checks passed!")
        exit(0)  # Exit with success status

if __name__ == "__main__":
    test_dagger_identity_product()
