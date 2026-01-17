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

def reproducer_sympy_issue():
    from sympy import symbols, expand, factor, Matrix, cos, sin, simplify, lambdify

    # Reproducing the factoring issue
    x, y = symbols('x y')
    z = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
    w = expand(z)
    v = factor(w)
    expanded_v = expand(v)
    try:
        assert expanded_v == w, "Factoring issue detected"
    except AssertionError as e:
        print("Factoring issue reproducible:")
        print_stacktrace(e)

    # Reproducing the simplify issue
    q_1, q_2, q_3 = symbols('q_1 q_2 q_3')
    q = [q_1, q_2, q_3]

    Mq = Matrix([
        [(1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*sin(q_1)**2 + (1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*cos(q_1)**2 + 0.25*sin(q_1)**2*cos(q_2)**2 + 0.25*cos(q_1)**2*cos(q_2)**2, 0, 0],
        [0, (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*sin(q_1)**2 + (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*cos(q_1)**2 + (-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))**2 + 0.25*sin(q_1)**2*sin(q_2)**2 + 0.25*sin(q_2)**2*cos(q_1)**2 + 0.25*cos(q_2)**2, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3)],
        [0, -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3), 0.25*sin(q_1)**2*sin(q_2 + q_3)**2 + 0.25*sin(q_2 + q_3)**2*cos(q_1)**2 + 0.25*cos(q_2 + q_3)**2]
    ])
    
    Mqs = simplify(Mq)
    Mq_fnc = lambdify(q, Mq, modules="numpy")
    Mqs_fnc = lambdify(q, Mqs, modules="numpy")
    
    correct_result = Mq_fnc(0, 0, 0)
    simplified_result = Mqs_fnc(0, 0, 0)
    
    try:
        assert (correct_result == simplified_result).all(), "Simplify issue detected"
    except AssertionError as e:
        print("Simplify issue reproducible:")
        print_stacktrace(e)

if __name__ == "__main__":
    reproducer_sympy_issue()
```

This python script tries to reproduce two issues with the `sympy` library related to polynomial factoring and the simplification of expressions. It raises an `AssertionError` when the output of an operation is incorrect compared to the expected result, allowing the detection of inconsistencies in the library's functionality. 

Please ensure that the Sympy package is up to date or matches the version mentioned in the original issues before running this script, as behavior may vary across versions.