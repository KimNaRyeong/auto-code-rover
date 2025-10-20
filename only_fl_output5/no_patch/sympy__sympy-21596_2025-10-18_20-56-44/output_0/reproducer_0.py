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

try:
    from sympy import symbols, I, imageset, Lambda, S

    # Define the set S1
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)

    # Check the presence of 2 in S1 directly
    assert 2 not in S1, "2 should not be in S1 directly"

    # Check the presence of 2 in S1 intersected with Reals
    assert 2 not in S1.intersect(S.Reals), "2 should not be in the intersection of S1 and Reals"

    # Check if the intersection of S1 and Reals is correct
    S2 = S.Reals
    intersection_result = S1.intersect(S2)
    expected_result = {-1, 1}
    assert intersection_result == expected_result, f"Intersection result is incorrect, got: {intersection_result}"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("No issues detected.")
    exit(0)
