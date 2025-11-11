import sympy as sy
import sys
from traceback import extract_tb, print_exception

def print_stacktrace(e):
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = extract_tb(e.__traceback__)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)
    expected_shape = (0, 6)
    actual_shape = sy.Matrix.hstack(M1, M2, M3, M4).shape
    if actual_shape != expected_shape:
        raise AssertionError("Expected shape: {}, Actual shape: {}".format(expected_shape, actual_shape))
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

try:
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)
    expected_shape = (0, 3)
    actual_shape = sy.Matrix.hstack(M1, M2, M3, M4).shape
    if actual_shape != expected_shape:
        raise AssertionError("Expected shape: {}, Actual shape: {}".format(expected_shape, actual_shape))
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

try:
    M1 = sy.Matrix.zeros(1, 0)
    M2 = sy.Matrix.zeros(1, 1)
    M3 = sy.Matrix.zeros(1, 2)
    M4 = sy.Matrix.zeros(1, 3)
    expected_shape = (1, 6)
    actual_shape = sy.Matrix.hstack(M1, M2, M3, M4).shape
    if actual_shape != expected_shape:
        raise AssertionError("Expected shape: {}, Actual shape: {}".format(expected_shape, actual_shape))
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Test passed.")
sys.exit(0)
