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

def test_matrix_normal_pdf():
    from sympy import MatrixSymbol, exp, pi, Matrix
    from sympy.stats import density, MatrixNormal
    import sympy as sp

    # Matrix Normal Distribution Parameters
    M = MatrixNormal('M', Matrix([[1, 2]]), Matrix([[1]]), Matrix([[1, 0], [0, 1]]))
    X = MatrixSymbol('X', 1, 2)

    # Getting the actual density
    actual_density = density(M)(X).doit()

    # Extract the coefficient of the exponent (to compare the normalization constant)
    # Since the normalizing constant is the part of the expression outside of exp(),
    # we simplify the expression under the assumption that the integration over all space = 1.
    try:
        # Attempt to get the coefficient directly assuming standard form
        constant_term = actual_density.as_coefficients_dict()[exp(1)]
    except:
        raise AssertionError("Failed to retrieve the constant term from the actual density.")

    # The expected normalization factor based on the given issue description is 1/(2*pi)
    expected_constant = 1/(2*pi)

    # Assert the normalization factor
    if sp.simplify(constant_term - expected_constant) != 0:
        raise AssertionError("Normalization factor in the PDF is incorrect.")

if __name__ == '__main__':
    try:
        test_matrix_normal_pdf()
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("The issue is either fixed, or the test did not reproduce the issue.")
        SystemExit(0)
