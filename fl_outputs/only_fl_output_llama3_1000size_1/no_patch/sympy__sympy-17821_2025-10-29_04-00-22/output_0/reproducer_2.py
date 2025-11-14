import doctest
from sympy import latex, Sum, S

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

def test_catalan_rewrite():
    try:
        from sympy.combinatorics import Catalan
        latex(Catalan().rewrite(Sum))
    except Exception as e:
        raise AssertionError("Catalan rewrite failed") from e

if __name__ == "__main__":
    try:
        test_catalan_rewrite()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
