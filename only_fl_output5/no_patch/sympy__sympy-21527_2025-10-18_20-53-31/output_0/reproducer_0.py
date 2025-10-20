import sympy


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


def reproduce_issue():
    x, y = sympy.symbols('x, y')

    solutions = []
    fractions = [0.0215, 0.0216, 0.0217]

    for fraction in fractions:
        solution = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, fraction * x)], (x, y))
        solutions.append(solution)

    expected_solution = sympy.FiniteSet((0, 0))
    for i, solution in enumerate(solutions):
        if solution != expected_solution:
            raise AssertionError(f"Solution for fraction {fractions[i]} does not match expected solution: {solution} != {expected_solution}")

    print("All solutions matched the expected solution.")


if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

    SystemExit(0)
