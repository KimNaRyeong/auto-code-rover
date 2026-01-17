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

def test_polynomial_factoring():
    import sympy as sp
    x, y = sp.symbols('x y')
    z = 0.0001 * (x * (x + 4.0 * y)) + 0.0001 * (y * (x + 4.0 * y))
    w = sp.expand(z)
    v = sp.factor(w)
    expanded_v = sp.expand(v)
    # Checking if the expansion of the factored expression matches the original expansion
    assert expanded_v == w, "Factoring and expansion results do not match the original expression."

def test_simplify_mass_matrix():
    from sympy import symbols, cos, sin, Matrix, simplify, lambdify
    q_1, q_2, q_3 = symbols('q_1 q_2 q_3')
    q = [q_1, q_2, q_3]

    Mq = Matrix([
        [(1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*sin(q_1)**2 + (1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*cos(q_1)**2 + 0.25*sin(q_1)**2*cos(q_2)**2 + 0.25*cos(q_1)**2*cos(q_2)**2, 0, 0],
        [0, (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*sin(q_1)**2 + (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*cos(q_1)**2 + (-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))**2 + 0.25*sin(q_1)**2*sin(q_2)**2 + 0.25*sin(q_2)**2*cos(q_1)**2 + 0.25*cos(q_2)**2, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3)],
        [0, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3), 0.25*sin(q_1)**2*sin(q_2 + q_3)**2 + 0.25*sin(q_2 + q_3)**2*cos(q_1)**2 + 0.25*cos(q_2 + q_3)**2]
    ])

    Mqs = simplify(Mq)
    Mqs_fnc = lambdify(q, Mqs)
    simplified_result = Mqs_fnc(0, 0, 0)

    # Asserting if the simplified matrix evaluated at 0, 0, 0 is not as expected
    expected_result = [[0.625, 0., 0.], [0., 2.5, 0.75], [0., 0.75, 0.25]]
    assert not (simplified_result == expected_result).all(), "Simplified matrix result is incorrect."

try:
    test_polynomial_factoring()
except AssertionError as e:
    print_stacktrace(e)

try:
    test_simplify_mass_matrix()
except AssertionError as e:
    print_stacktrace(e)
