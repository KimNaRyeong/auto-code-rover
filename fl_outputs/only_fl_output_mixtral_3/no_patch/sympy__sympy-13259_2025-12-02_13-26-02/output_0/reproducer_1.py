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

def main():
    a = 2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3
    expected_a = -0.333333333333333 + 1.0*I
    assert abs(a.evalf() - expected_a) < 1e-12, "a should equal expected_a numerically"

    b = a.simplify()
    expected_b = 1.6818694524863*I
    assert abs(b.evalf() - expected_b) < 1e-12, "b should equal expected_b numerically"

    assert a == b, "a should equal b numerically"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
