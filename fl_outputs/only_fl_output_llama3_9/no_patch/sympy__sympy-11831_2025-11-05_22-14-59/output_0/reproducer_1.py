import sympy as sp

def print_stacktrace(e):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f"  File '{frame.filename}'")
        print(f"    {line_number}: {code_context}")
    print(f"{e.__class__.__name__}: {e}")

try:
    d = sp.symbols("d")
    solution = sp.FiniteSet((d + 1, -d + 4, -d + 5, d))
    solution.intersect(sp.Naturals0**4)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected TypeError"
    exit(1)

print("Issue not reproduced")
exit(0)
