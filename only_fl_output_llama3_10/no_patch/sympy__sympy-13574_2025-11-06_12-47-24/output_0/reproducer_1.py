import sympy
from sympy.matrices import randMatrix

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

def reproduce_issue():
    try:
        assert sympy.Matrix([[1, 0], [0, 1]]).equals(sympy.Matrix([[1, 0], [0, 1]]))
        for i in range(3):
            if i == 0:
                percent = 1
            elif i == 1:
                percent = 50
            else:
                percent = 99
            matrix = randMatrix(i+1, symmetric=True, percent=percent)
            assert matrix.equals(matrix.T), f"Symmetric matrix not generated for percent {percent}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
