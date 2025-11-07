import sympy
from sympy.algebras.quaternion import Quaternion
from sympy import symbols, cos, sin
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    sympy_version = sympy.__version__
    print('Sympy version: ', sympy_version)

    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    rotation_matrix = sympy.trigsimp(q.to_rotation_matrix())

    expected_matrix = sympy.Matrix([
        [1,      0,       0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]])

    try:
        assert rotation_matrix == expected_matrix, "Rotation matrix does not match the expected output."
        print("The issue appears to be fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # exit with code 0 when the issue is fixed, change to sys.exit(1) if you want it to exit with an error code when the issue is detected

if __name__ == "__main__":
    main()
