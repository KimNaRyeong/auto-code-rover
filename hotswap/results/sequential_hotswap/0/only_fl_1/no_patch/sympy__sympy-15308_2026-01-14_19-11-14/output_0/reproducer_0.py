from sympy import MatrixSymbol, trace, latex

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

def main():
    n = 3  # Assume a value for n, since n is not defined in the example
    A = MatrixSymbol("A", n, n)
    expected_latex = r'\operatorname{trace}\left(A^{2}\right)'  # Assuming the expected correct LaTeX output
    generated_latex = latex(trace(A**2))

    try:
        assert generated_latex == expected_latex, "LaTeX generation for matrix expression is incorrect"
        print("Issue fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate error

if __name__ == "__main__":
    main()
