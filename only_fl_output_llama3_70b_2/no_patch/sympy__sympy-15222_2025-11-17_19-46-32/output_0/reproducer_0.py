from sympy import symbols, Subs

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

x, y, a, z = symbols('x y a z')

try:
    subs = Subs(x+y,(a,),(4,))
    result = subs.subs(a,z)
    assert str(result) == "Subs(x + y, (a,), (z,))", f"Expected Subs(x + y, (a,), (z,)), but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
