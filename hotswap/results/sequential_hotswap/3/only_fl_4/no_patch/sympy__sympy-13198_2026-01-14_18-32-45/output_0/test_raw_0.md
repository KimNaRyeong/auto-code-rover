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

def test_polynomial_factoring_issue():
    import sympy as sp
    x, y = sp.symbols('x y')
    z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
    w = sp.expand(z)
    v = sp.factor(w)
    expanded_v = sp.expand(v)
    # Assert the expanded form of the factored polynomial matches the original expanded form.
    try:
        assert expanded_v == w, "Factoring and expansion did not match original expression"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if the assertion fails.

def test_matrix_simplification_issue():
    from sympy import Symbol, Matrix, sin, cos, simplify, lambdify
    q_1, q_2, q_3 = Symbol('q_1'), Symbol('q_2'), Symbol('q_3')
    q = [q_1, q_2, q_3]

    Mq = Matrix([
        [(1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*sin(q_1)**2 + (1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*cos(q_1)**2 + 0.25*sin(q_1)**2*cos(q_2)**2 + 0.25*cos(q_1)**2*cos(q_2)**2, 0, 0],
        [0, (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*sin(q_1)**2 + (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*cos(q_1)**2 + (-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))**2 + 0.25*sin(q_1)**2*sin(q_2)**2 + 0.25*sin(q_2)**2*cos(q_1)**2 + 0.25*cos(q_2)**2, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3)],
        [0, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3), 0.25*sin(q_1)**2*sin(q_2 + q_3)**2 + 0.25*sin(q_2 + q_3)**2*cos(q_1)**2 + 0.25*cos(q_2 + q_3)**2]
    ])

    Mq_fnc = lambdify(q, Mq)
    correct_result = [[2.5, 0., 0.], [0., 2.5, 0.75], [0., 0.75, 0.25]]

    Mqs = simplify(Mq)
    Mqs_fnc = lambdify(q, Mqs)
    simplified_result = Mqs_fnc(0, 0, 0)

    try:
        assert simplified_result == correct_result, "Simplified matrix evaluation did not match expected result"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if the assertion fails.

if __name__ == "__main__":
    test_polynomial_factoring_issue()
    test_matrix_simplification_issue()
    print("All tests passed successfully.")
    exit(0)
```