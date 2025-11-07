import sympy
from sympy import symbols, Eq, linsolve

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

def test_linsolve_consistency():
    x, y = symbols('x y')
    results = []

    # Define the equations with slight variations in the multiplier of x
    multipliers = [0.0215, 0.0216, 0.0217]
    for multiplier in multipliers:
        result = linsolve([Eq(y, x), Eq(y, multiplier * x)], (x, y))
        results.append(result)

    # Expect all results to be the same, indicating consistent behavior
    try:
        assert results[0] == results[1] == results[2], "linsolve failed to maintain consistency across similar equations"
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_linsolve_consistency()
