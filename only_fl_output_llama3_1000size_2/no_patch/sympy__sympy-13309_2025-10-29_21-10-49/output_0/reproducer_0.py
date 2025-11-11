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

try:
    from sympy import Max
    result = Max(1, 2).rewrite(sp.Piecewise)
    assert result == sp.Piecewise((1, True), (2, False)), "Expected Max(a, b) to be rewritten as Piecewise((a, a>b), (b, True))"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
