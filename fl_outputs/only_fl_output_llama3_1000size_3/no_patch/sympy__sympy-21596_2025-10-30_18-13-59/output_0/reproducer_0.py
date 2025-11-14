import sympy as sp

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

def reproduce_issue():
    try:
        S1 = sp.imageset(lambda n: n + (n - 1)*(n + 1)*sp.I, sp.S.Integers)
        if not isinstance(S1, set):
            raise AssertionError("Expected a set but got {}".format(type(S1)))
        print(f"S1: {S1}")
        if 2 in S1:
            raise AssertionError("2 is expected to be False")
        if 2 in S1.intersect(sp.Reals):
            raise AssertionError("2 is expected to be False in the intersection with Reals")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
