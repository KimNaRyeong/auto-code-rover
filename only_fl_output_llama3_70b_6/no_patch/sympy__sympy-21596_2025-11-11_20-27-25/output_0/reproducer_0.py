from sympy import Lambda, I, S, imageset, Integers, Reals

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
    S1 = imageset(Lambda('n', 'n + (n - 1)*(n + 1)*I'), S.Integers)
    assert not (2 in S1), "Expected 2 not to be in S1"
    assert not (2 in S1.intersect(Reals)), "Expected 2 not to be in S1 intersect Reals"
    S2 = Reals
    assert set(S1.intersect(S2)) == {-1, 1}, "Expected intersection of S1 and Reals to be {-1, 1}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
