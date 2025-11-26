from sympy import Lambda, I, S, imageset

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
    assert not (2 in S1.intersect(S.Reals)), "Expected 2 not to be in S1 intersect Reals"
    print("Issue is fixed")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
