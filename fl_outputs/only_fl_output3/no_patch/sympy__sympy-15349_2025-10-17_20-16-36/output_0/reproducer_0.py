# reproducer.py

import sympy
from sympy import symbols, cos, sin, trigsimp, Quaternion
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
    print('Sympy version: ', sympy.__version__)
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    expected_matrix = sympy.Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    
    result_matrix = trigsimp(q.to_rotation_matrix())
    try:
        assert expected_matrix == result_matrix, "Result matrix does not match the expected output."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status
    print("Test passed.")

if __name__ == "__main__":
    main()
