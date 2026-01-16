# reproducer.py
import sys
from sympy import symbols, sqrt, lambdify, N
from mpmath import mp

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

def main():
    x = symbols('x')
    g = sqrt(2) - x
    h = g.evalf(64)

    f1 = lambdify(x, g, modules='mpmath')
    f2 = lambdify(x, h, modules='mpmath')

    # Increase mpmath precision to match the required precision
    mp.dps = 64
    result_f1 = f1(N(sqrt(2), 64))
    result_f2 = f2(N(sqrt(2), 64))

    # Condition that triggers if the issue is present
    try:
        # Assert the difference is beyond the threshold of double precision
        assert abs(result_f1 - result_f2) < mp.mpf('1.0e-64'), "Precision loss detected"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code indicating failure/assertion failure

    print("No precision loss detected. Issue resolved or not present.")
    sys.exit(0)

if __name__ == "__main__":
    main()
