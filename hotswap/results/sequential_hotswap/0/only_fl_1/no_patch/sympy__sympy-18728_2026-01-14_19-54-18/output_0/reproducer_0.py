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
    from sympy import Symbol, symbols, zoo

    try:
        # Case 1: Assertion for wrong handling of is_zero for Pow
        a, b = symbols('a b', positive=True)
        assert (a**b).is_zero is None, "Incorrect assumption for a**b is_zero."

        # Case 2: Assertion for the fix provided for #9532
        # Symbol with real=True should correctly handle division with zoo
        n = Symbol('n', real=True, finite=True)
        assert zoo / n == zoo, "Incorrect behavior for zoo / n."

        # Case 3: Assertion for potential incorrect handling of finite assumption
        n = Symbol('n', finite=True)
        assert (zoo / n).is_finite is None, "Incorrect handling of finiteness with zoo / n."

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
