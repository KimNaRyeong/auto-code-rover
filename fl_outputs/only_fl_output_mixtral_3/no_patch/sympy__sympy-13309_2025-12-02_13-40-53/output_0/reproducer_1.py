import sympy as sp
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_max_rewrite():
    a, b = sp.symbols('a b')
    max_ab = sp.Max(a, b)
    piecewise_ab = sp.Piecewise((a, a > b), (b, True))
    max_ab_rewritten = max_ab.rewrite(sp.Piecewise)
    assert max_ab_rewritten == piecewise_ab, "Max rewriting for Piecewise is incorrect"

if __name__ == "__main__":
    try:
        test_max_rewrite()
        print("Test passed")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
