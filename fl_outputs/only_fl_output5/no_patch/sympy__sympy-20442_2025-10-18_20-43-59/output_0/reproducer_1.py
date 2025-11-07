from sympy import symbols, Rational
from sympy.physics.units import convert_to, joule, s, kg, m

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

def validate_conversion():
    # Correction to correctly import and use convert_to
    # Define joule in terms of kg, m, and s
    J = kg*m**2/s**2
    J_s = J * s

    # Try conversion and check for expected behavior
    try:
        converted = convert_to(J_s, J)
        # The issue described happens here; instead of J_s or an understandable unit, it returns J**(7/9)
        assert converted != J**(Rational(7,9)), "Conversion returned unexpected joule powers"
        assert converted == J_s, "Conversion did not return expected result of J*s"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    print("No issue detected. The conversion behaves as expected.")

if __name__ == "__main__":
    validate_conversion()
