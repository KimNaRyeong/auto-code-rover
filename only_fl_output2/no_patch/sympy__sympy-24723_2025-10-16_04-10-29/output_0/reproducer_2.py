# reproducer.py

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
    from sympy import MatrixSymbol, symbols, pi
    from sympy.stats import density, MatrixNormal
    X = MatrixSymbol('X', 1, 2)
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    pdf = density(M)(X).doit()

    # Expected parts of the PDF expression
    _, two_pi_constant = symbols('e 2_pi')
    two_pi_exp = 2 * pi

    try:
        # Locate the 2*pi expression
        if not two_pi_constant in pdf.free_symbols or two_pi_exp not in pdf.atoms():
            raise AssertionError("PDF expression does not contain expected 2*pi component.")
    except AssertionError as e:
        print("PDF validation failed:")
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_matrix_normal_pdf()
    print("PDF validation passed: Issue is fixed or was not present.")
