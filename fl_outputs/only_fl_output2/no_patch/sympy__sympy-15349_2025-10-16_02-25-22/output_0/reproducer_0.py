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
    import sympy
    from sympy import symbols, cos, sin, trigsimp

    print('Sympy version: ', sympy.__version__)

    x = symbols('x')
    q = sympy.Quaternion(cos(x/2), sin(x/2), 0, 0)
    result_matrix = trigsimp(q.to_rotation_matrix())
    
    # Expected matrix
    expected_matrix = sympy.Matrix([
        [1,      0,       0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]])

    try:
        assert result_matrix == expected_matrix
        print("Issue fixed.")
    except AssertionError as e:
        print("Issue present. Incorrect result from Quaternion.to_rotation_matrix().")
        print("Expected matrix:\n", expected_matrix)
        print("Result matrix:\n", result_matrix)
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
