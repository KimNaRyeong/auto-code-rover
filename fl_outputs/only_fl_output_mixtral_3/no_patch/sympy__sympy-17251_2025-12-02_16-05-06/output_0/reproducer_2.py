import sys
import traceback
from sympy import exp, I, pi, simplify, Rational, expand_complex

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_exp_simplify():
    e1 = exp(Rational(9, 1) * I * pi / 4)
    e2 = simplify(e1)
    assert e1 == e2, "exp doesn't simplify based on its periodicity"

    a = e1 - exp(I * pi / 4)
    e3 = simplify(a)
    e4 = expand_complex(a)
    assert e3 == e4, "exp doesn't use its periodicity to reduce its argument"

if __name__ == "__main__":
    try:
        test_exp_simplify()
        print("No issues found.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
