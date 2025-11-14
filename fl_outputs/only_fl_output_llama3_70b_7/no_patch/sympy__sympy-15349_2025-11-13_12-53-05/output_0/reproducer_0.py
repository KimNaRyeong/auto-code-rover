import sympy
from sympy import symbols, Quaternion

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
    x = symbols('x')
    q = Quaternion(sympy.cos(x/2), sympy.sin(x/2), 0, 0)
    rotation_matrix = q.to_rotation_matrix()
    expected_matrix = sympy.Matrix([
        [1,      0,      0],
        [0, sympy.cos(x), -sympy.sin(x)],
        [0, sympy.sin(x),  sympy.cos(x)]
    ])
    
    try:
        assert rotation_matrix.equals(expected_matrix)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
