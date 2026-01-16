from sympy import symbols, Poly, S

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

def check_poly_multiplication():
    x = symbols('x')
    try:
        # Poly multiplied from the left by x
        result_left = x*Poly(x)
        expected_left = Poly(x**2, x, domain='ZZ')
        
        # Poly multiplied from the right by x
        result_right = Poly(x)*x
        expected_right = Poly(x**2, x, domain='ZZ')

        # Ensuring that multiplication behaves correctly from both sides
        assert result_left == expected_left, "Multiplying expression by Poly on the left side fails."
        assert result_right == expected_right, "Multiplying Poly by expression on the right side fails."

        # Additional checks for consistency with scalars
        negative_scalar_result_left = S(-2)*Poly(x)
        negative_scalar_expected_left = Poly(-2*x, x, domain='ZZ')
        
        negative_scalar_result_right = Poly(x)*S(-2)
        negative_scalar_expected_right = Poly(-2*x, x, domain='ZZ')

        assert negative_scalar_result_left == negative_scalar_expected_left, "Multiplying S(-2) by Poly on the left side fails."
        assert negative_scalar_result_right == negative_scalar_expected_right, "Multiplying Poly by S(-2) on the right side fails."

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        check_poly_multiplication()
        print("No issue found.")
    except AssertionError:
        exit(1)
