from sympy import *
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = Symbol('x')
M = Matrix([[x, 0, 1], [x, 0, 2], [exp(x), 1, 0]])

try:
    eigenvals = M.eigenvals()
except Exception as e:
    print_stacktrace(e)
    assert False, "MatrixError should not be raised here"

try:
    charpoly = M.charpoly()
except NotImplementedError as e:
    print_stacktrace(e)
    assert False, "NotImplementedError should not be raised here"

roots = list(roots(charpoly))
if not roots:
    assert False, "roots(M.charpoly()) should return three roots of the characteristic polynomial"
