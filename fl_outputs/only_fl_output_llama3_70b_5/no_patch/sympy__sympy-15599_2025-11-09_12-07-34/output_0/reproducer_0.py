from sympy import Symbol, Mod

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

def test_Mod():
    i = Symbol('i', integer=True)
    assert Mod(3*i, 2) == Mod(i, 2), "Mod(3*i, 2) should reduce to Mod(i, 2)"

try:
    test_Mod()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
