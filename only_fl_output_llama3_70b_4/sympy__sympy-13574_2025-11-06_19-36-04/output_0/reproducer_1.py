import sympy
from sympy.matrices import randMatrix

def test_symmetric_matrix(percent):
    matrix = randMatrix(3, symmetric=True, percent=percent)
    assert (matrix.T == matrix), f"Matrix is not symmetric for percent={percent}"

try:
    test_symmetric_matrix(1)
    test_symmetric_matrix(50)
    test_symmetric_matrix(99)
    test_symmetric_matrix(0)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)


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
