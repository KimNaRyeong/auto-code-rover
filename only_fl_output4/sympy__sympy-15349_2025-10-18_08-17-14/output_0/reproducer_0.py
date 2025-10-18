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

def test_quaternion_to_rotation_matrix():
    import sympy
    from sympy import symbols, cos, sin, Quaternion, trigsimp

    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    rotation_matrix = trigsimp(q.to_rotation_matrix())

    # Expecting one of the sin(x) to be negative for correct rotation matrix
    expected_matrix = sympy.Matrix([
        [1,       0,        0],
        [0,  cos(x), -sin(x)],
        [0,  sin(x),  cos(x)]
    ])

    assert rotation_matrix == expected_matrix, "Quaternion.to_rotation_matrix() output is incorrect."

if __name__ == '__main__':
    try:
        test_quaternion_to_rotation_matrix()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    print("Test passed. The issue is fixed.")
    exit(0)
