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

def main():
    from sympy import symbols, MatrixSymbol, latex

    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)

    try:
        generated_latex = latex((M*N)[i, j])
        # Check for the specific problematic pattern in the generated LaTeX string.
        assert "\sum_{i_{1}=0}^{k - 1} M_{i, _i_1} N_{_i_1, j}" != generated_latex, "Issue with LaTeX subscript rendering detected."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 indicating failure/reproduction of the issue

    print("Issue fixed or not present.")
    sys.exit(0)  # Exit with code 0 indicating no issue detected

if __name__ == "__main__":
    main()
