from sympy import Max, Piecewise, symbols

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

a, b = symbols('a b')

try:
    result = Max(a, b).rewrite(Piecewise)
    assert str(result) == "Piecewise((a, a>b), (b, True))", f"Expected Piecewise((a, a>b), (b, True)), but got {result}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
