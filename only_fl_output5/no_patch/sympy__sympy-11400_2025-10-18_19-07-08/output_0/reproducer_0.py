from sympy import symbols, ccode, sinc, Piecewise, sin, Ne
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

def test_sinc_code_generation():
    x = symbols('x')
    try:
        generated_code = ccode(sinc(x))
        # The expected snippet might need to be adapted based on the desired output; below is an example
        expected_snippet = '((Ne(x, 0)) ? (\n   sin(x)/x\n)\n: (\n   1\n))'
        piecewise_code = ccode(Piecewise((sin(x)/x, Ne(x, 0)), (1, True)))

        assert generated_code == expected_snippet, "Generated code does not match expected output."
        assert generated_code == piecewise_code, "Generated code does not match Piecewise equivalent."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sinc_code_generation()
    except AssertionError:
        sys.exit(1)  # Exits with a non-zero code if the issue is present.
    else:
        print("Success: The issue is fixed.")
        sys.exit(0)  # Exits with code 0 when the issue is fixed.
