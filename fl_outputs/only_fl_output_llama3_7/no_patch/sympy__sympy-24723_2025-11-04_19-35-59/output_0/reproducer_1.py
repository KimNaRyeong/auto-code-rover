from sympy import MatrixSymbol, I, eye
from sympy.stats import density, MatrixNormal
import sys

def print_stacktrace(e):
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
    M = MatrixNormal('M', [[1, 2]], [1], [[1, 0], [0, 1]])
    X = MatrixSymbol('X', 1, 2)
    result = density(M)(X).doit()
    if result != "       ⎛⎛⎡-1⎤    T⎞                ⎞\n" \
               "   -tr ⎜⎜⎢  ⎥ + X ⎟ ⋅([-1  -2] + X)⎟\n" \
               "       ⎝⎝⎣-2⎦     ⎠                ⎠\n" \
               "    ────────────────────────────────\n" \
               "                  2\n" \
               "2ℯ\n" \
               " ───────────────────────────────────\n" \
               "                 π\n":
        raise AssertionError("Matrix Normal Distribution returns wrong probability density function")
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
