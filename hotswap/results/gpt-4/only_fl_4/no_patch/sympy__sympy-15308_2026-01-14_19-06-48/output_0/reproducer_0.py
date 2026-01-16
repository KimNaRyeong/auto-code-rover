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

def test_matrix_expression_latex_printing():
    from sympy import MatrixSymbol, trace, latex

    A = MatrixSymbol("A", n, n)
    
    expected_latex_string = '\\text{Trace}\\left(A^{2}\\right)' # The expected outcome might differ based on the actual LaTeX printing conventions and fixes
    actual_latex_string = latex(trace(A**2))

    assert actual_latex_string == expected_latex_string, \
        f"LaTeX printing for matrix expressions is broken. Expected: '{expected_latex_string}', got: '{actual_latex_string}'"

if __name__ == "__main__":
    try:
        # Assuming that `n` is defined globally for simplicity, real use cases should define `n` properly
        n = 3   # a placeholder value to make the symbol n concrete
        test_matrix_expression_latex_printing()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    except Exception as e:
        print("An unexpected exception occurred:")
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("No issue detected.")
