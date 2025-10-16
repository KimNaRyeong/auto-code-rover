def main():
    from sympy import symbols, imageset, Lambda, I, S
    from sympy.abc import n

    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)

    try:
        assert 2 not in S1, "Assertion failed: 2 was found in S1, but it shouldn't be."

        # Correct behavior should not find 2 in the intersection of S1 and Reals
        assert 2 not in S1.intersect(S.Reals), "Assertion failed: 2 was found in the intersection of S1 and Reals."

        # Check the intersection of S1 and Reals to see whether it's as expected
        intersection = S1.intersect(S.Reals)
        assert intersection == {-1, 1}, f"Assertion failed: The intersection of S1 and Reals was expected to be {-1, 1}, but was {intersection}."

        print("All checks passed. The issue appears to be fixed.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Ensure the script exits with a non-zero code if an assertion fails

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

if __name__ == "__main__":
    main()
