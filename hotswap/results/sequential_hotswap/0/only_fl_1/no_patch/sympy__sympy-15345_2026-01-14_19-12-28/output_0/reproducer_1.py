# reproducer.py
from sympy import symbols, Max
from sympy.printing.mathematica import mathematica_code

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

def test_mathematica_code_with_max():
    x = symbols('x')
    try:
        output = mathematica_code(Max(x, 2))
        # Given the issue, this check will potentially fail because of incorrect Mathematica syntax generation.
        assert output == 'Max[x, 2]', f"Incorrect Mathematica code generated: {output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_mathematica_code_with_max()
    except AssertionError:
        # If an AssertionError is caught, it implies the issue is present.
        exit(1) # Non-zero exit code indicates failure
    exit(0) # Exit code 0 indicates success/no error
