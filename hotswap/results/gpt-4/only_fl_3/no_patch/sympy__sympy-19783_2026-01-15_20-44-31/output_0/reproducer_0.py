import sys

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

def test_dagger_identity():
    from sympy.physics.quantum.dagger import Dagger
    from sympy.physics.quantum.operator import Operator
    from sympy.physics.quantum import IdentityOperator
    try:
        # Define operator A and its dagger
        A = Operator('A')
        B = Dagger(A)
        
        # Define the identity operator
        Identity = IdentityOperator()
        
        # Multiply B by the identity and check if the result is not simplified
        result = B * Identity
        
        # Checking if the multiplication is simplified correctly
        # Raising an AssertionError if it is not
        assert str(result) == "Dagger(A)", "Multiplication with Identity Operator is not simplified."
        print("Test Passed: Dagger() * IdentityOperator() simplified correctly.")
    
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_dagger_identity()
