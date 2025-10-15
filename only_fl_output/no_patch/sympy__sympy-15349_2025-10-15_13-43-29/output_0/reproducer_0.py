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

try:
    import sympy
    print('Sympy version:', sympy.__version__)
    from sympy import symbols, cos, sin, trigsimp
    from sympy.algebras.quaternion import Quaternion

    # Define symbol
    x = symbols('x')

    # Create a Quaternion
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)

    # Convert the Quaternion to a rotation matrix and simplify it
    rotation_matrix = trigsimp(q.to_rotation_matrix())

    # Expected rotation matrix
    expected_matrix = sympy.Matrix([
        [1,      0,       0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]
    ])

    # Assert the correctness of the rotation matrix
    assert rotation_matrix == expected_matrix, "The rotation matrix does not match the expected result."

except AssertionError as e:
    print_stacktrace(e)
    raise

except Exception as e:
    print_stacktrace(e)
    exit(1)

print("The issue does not exist.")
exit(0)
