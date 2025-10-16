from sympy import symbols, sinc, ccode, Piecewise, Ne, sin
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

def reproduce_sinc_issue():
    x = symbols('x')
    generated_code = ccode(sinc(x))
    expected_code_for_sinc = '((Ne(x, 0)) ? (\n   sin(x)/x\n)\n: (\n   1\n))'
    try:
        assert generated_code == expected_code_for_sinc, "sinc function C code generation does not match expected output."
        print("Issue fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status when the assertion fails indicating the issue is still present.

def reproduce_piecewise_issue():
    theta = symbols('theta')
    pw = Piecewise((sin(theta)/theta, Ne(theta, 0)), (1, True))
    generated_code = ccode(pw)
    expected_code_for_piecewise = '((Ne(theta, 0)) ? (\n   sin(theta)/theta\n)\n: (\n   1\n))'
    try:
        assert generated_code == expected_code_for_piecewise, "Piecewise C code generation does not match expected output."
        print("Issue fixed for Piecewise equivalent.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status when the assertion fails indicating the specific Piecewise issue is still present.

if __name__ == "__main__":
    reproduce_sinc_issue()
    # You can call reproduce_piecewise_issue() similarly if needed.
