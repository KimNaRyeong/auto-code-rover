```python
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
    x, y = sympy.symbols('x, y')

    # Defining the equations
    equations_1 = [sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)]
    equations_2 = [sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)]
    equations_3 = [sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)]

    # Attempting to solve the equations
    solution_1 = sympy.linsolve(equations_1, (x, y))
    solution_2 = sympy.linsolve(equations_2, (x, y))
    solution_3 = sympy.linsolve(equations_3, (x, y))

    try:
        # Expecting all solutions to be FiniteSet((0, 0))
        assert solution_1 == sympy.FiniteSet((0, 0)), "Unexpected result for equations_1"
        assert solution_2 == sympy.FiniteSet((0, 0)), "Unexpected result for equations_2"
        assert solution_3 == sympy.FiniteSet((0, 0)), "Unexpected result for equations_3"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sympy_linsolve()
    except AssertionError:
        exit(1)
    print("All tests passed successfully.")
    exit(0)
```