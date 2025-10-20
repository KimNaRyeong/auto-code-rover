from sympy import symbols, tan, RootOf

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

def test_rootof_ignores_generator_issue():
    x = symbols('x')
    try:
        # Test case 1
        root1 = RootOf(x**3 + x - 1, 0)
        if root1.poly.gen != x:
            raise AssertionError(f"RootOf does not recognize 'x' as its generator: {root1.poly.gen}")

        # Test case 2 - The generator should be tan(x) but checks if it mistakenly keeps it as x
        root2 = RootOf((x**3+x-1).subs(x, tan(x)), 0)
        if root2.poly.gen == x:
            raise AssertionError("RootOf incorrectly identifies 'x' as its generator instead of 'tan(x)'")

        # Test case 3 - Directly checking if the generator of the polynomial is maintained correctly
        root3 = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
        if root3.poly.gen != tan(x):
            raise AssertionError(f"Incorrect generator for the polynomial, expected 'tan(x)', found: {root3.poly.gen}")

        # Test case 4 - The issue highlighted, where the generator should be x but is erroneously tan(x)
        root4 = RootOf((x**3 + 2*x - 1).subs(x, tan(x)), 0)
        if root4.poly.gen != tan(x):
            raise AssertionError(f"RootOf changes its generator to {root4.poly.gen} instead of 'tan(x)'")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_rootof_ignores_generator_issue()
    print("No issue detected.")
    exit(0)
