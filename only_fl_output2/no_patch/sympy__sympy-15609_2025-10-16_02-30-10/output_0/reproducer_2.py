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

    # Define symbols and matrices
    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)

    # Produce the LaTeX representation and check it for errors
    try:
        latex_str = latex((M*N)[i, j])
        # Searching specifically for the double subscript error in the generated LaTeX string
        if '_{_' in latex_str:
            raise AssertionError("LaTeX string has double subscript which is not compilable.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code 1 as issue is reproduced

    # Exiting with code 0 if the issue is not found indicating it's fixed
    print("Issue not present, exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
