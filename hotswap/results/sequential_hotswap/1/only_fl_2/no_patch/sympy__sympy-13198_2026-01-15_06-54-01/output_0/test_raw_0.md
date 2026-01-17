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

def main():
    from sympy import symbols, cos, sin, Matrix, simplify, lambdify

    # Define symbols
    q_1, q_2, q_3 = symbols('q_1 q_2 q_3')

    # Define mass matrix
    Mq = Matrix([[
        (1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*sin(q_1)**2 + 
        (1.0*cos(q_2) + 0.5*cos(q_2 + q_3))**2*cos(q_1)**2 + 
        0.25*sin(q_1)**2*cos(q_2)**2 + 
        0.25*cos(q_1)**2*cos(q_2)**2, 
        0, 0
    ], [
        0, 
        (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*sin(q_1)**2 + 
        (-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))**2*cos(q_1)**2 + 
        (-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))**2 + 
        0.25*sin(q_1)**2*sin(q_2)**2 + 
        0.25*sin(q_2)**2*cos(q_1)**2 + 
        0.25*cos(q_2)**2,
        -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 
        0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 
        0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3)
    ], [
        0, 
        -0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_1)**2*sin(q_2 + q_3) - 
        0.5*(-1.0*sin(q_2) - 0.5*sin(q_2 + q_3))*sin(q_2 + q_3)*cos(q_1)**2 - 
        0.5*(-1.0*cos(q_2) - 0.5*cos(q_2 + q_3))*cos(q_2 + q_3), 
        0.25*sin(q_1)**2*sin(q_2 + q_3)**2 + 
        0.25*sin(q_2 + q_3)**2*cos(q_1)**2 + 
        0.25*cos(q_2 + q_3)**2
    ]])

    # Calculate original results
    Mq_fnc = lambdify([q_1, q_2, q_3], Mq)
    original_result = Mq_fnc(0, 0, 0)

    # Simplify the matrix and re-calculate
    Mqs = simplify(Mq)
    Mqs_fnc = lambdify([q_1, q_2, q_3], Mqs)
    simplified_result = Mqs_fnc(0, 0, 0)

    try:
        # The expected result after simplification should match the original calculation
        assert original_result.tolist() == simplified_result.tolist(), "Simplified matrix calculation does not match original"
        print("Issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```