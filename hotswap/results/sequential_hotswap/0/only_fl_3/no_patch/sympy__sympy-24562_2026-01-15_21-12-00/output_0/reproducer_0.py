# reproducer.py
import sympy as sp

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

def test_sympy_rational():
    try:
        # Create two fractions using Rational in two different ways
        frac_str = sp.Rational('0.5', '100')
        frac_float = sp.Rational(0.5, 100)

        # The expected value based on sympy's documentation and previous versions behavior
        correct_value = sp.Rational(1, 200)

        # Check if the values are as expected
        assert frac_str == correct_value, f"frac_str is {frac_str}, but expected {correct_value}"
        assert frac_float == correct_value, f"frac_float is {frac_float}, but expected {correct_value}"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_sympy_rational()

