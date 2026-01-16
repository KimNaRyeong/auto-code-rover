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
    from sympy import MatrixSymbol, MatAdd

    A = MatrixSymbol('A', 2, 2)

    # The core issue is that MatAdd(A, A, evaluate=True) should simplify to 2*A, but currently does not.
    try:
        result = MatAdd(A, A, evaluate=True)
        # If the issue exists, result will not simplify to '2*A', and hence the assertion will fail.
        assert str(result) != 'A + A', "Issue with MatAdd not evaluating correctly with 'evaluate=True'"
        print("The issue seems to be fixed as the assertion didn't fail.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate an error state due to the presence of the issue

if __name__ == "__main__":
    main()
