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

def test_sympy_linsolve():
    import sympy
    import sys
    x, y = sympy.symbols('x y')

    solution1 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)], (x, y))
    solution2 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)], (x, y))
    solution3 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)], (x, y))

    # Asserting that all solutions should be the same based on the theoretical expectation
    try:
        assert solution1 == sympy.FiniteSet((0, 0)), f'Expected {(0, 0)}, got {solution1}'
        assert solution2 == sympy.FiniteSet((0, 0)), f'Expected {(0, 0)}, got {solution2}'
        assert solution3 == sympy.FiniteSet((0, 0)), f'Expected {(0, 0)}, got {solution3}'

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code 1 if there is an AssertionError

    print("Issue fixed. Exiting with code 0.")
    sys.exit(0)  # Exit with code 0 when the issue is fixed

if __name__ == "__main__":
    test_sympy_linsolve()
