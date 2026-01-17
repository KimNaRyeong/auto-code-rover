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
    from sympy import ZeroMatrix

    Z = ZeroMatrix(2, 3)
    Ze = Z.as_explicit()

    # Assertions
    try:
        assert bool(Z) == True, "ZeroMatrix instance evaluates to False in boolean context, expected True"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    try:
        assert bool(Ze) == True, "Explicit ZeroMatrix evaluates to False in boolean context, expected True"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("Issue not present, exiting with code 0.")

if __name__ == "__main__":
    main()
