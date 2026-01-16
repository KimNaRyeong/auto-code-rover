from sympy import exp, Matrix, simplify, sin, cos, I
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

def check_sin_recognition():
    # Define the matrix to exponentiate
    m = exp(Matrix([[0, -I, 0], [I, 0, 0], [0, 0, 0]]))
    simplified_m = simplify(m)

    # After simplification, the matrix should express sin and cos correctly
    # The element at position [1, 0] and [0, 1] represents sin and -sin respectively
    expected_sin = sin(1)
    expected_minus_sin = -sin(1)

    sin_position = simplified_m[1, 0]
    minus_sin_position = simplified_m[0, 1]

    # Check if the simplification produces the expected results for sin(1) and -sin(1)
    if not (sin_position.has(expected_sin) and minus_sin_position.has(expected_minus_sin)):
        raise AssertionError("Simplification failed to recognize sin expressed as exponentials correctly.")

try:
    check_sin_recognition()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error code when issue is present
else:
    print("Issue fixed or not present.")
    sys.exit(0)  # Exit normally if issue is fixed

