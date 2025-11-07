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


def test_linsolve():
    x, y = sympy.symbols('x, y')
    result_1 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0215 * x)], (x, y))
    result_2 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0216 * x)], (x, y))
    result_3 = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, 0.0217 * x)], (x, y))
    
    expected_solution = sympy.FiniteSet((0, 0))

    errors = []

    if result_1 != expected_solution:
        errors.append(f"result_1: {result_1}")
    if result_2 != expected_solution:
        errors.append(f"result_2: {result_2}")
    if result_3 != expected_solution:
        errors.append(f"result_3: {result_3}")
    
    if errors:
        error_message = "Unexpected solutions found:\n" + "\n".join(errors)
        raise AssertionError(error_message)

try:
    test_linsolve()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("All systems of equations return the expected solution.")
    exit(0)
