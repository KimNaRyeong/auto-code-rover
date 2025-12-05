from math import pi, e
from sympy import latex
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        result = pi**(1/e)
        expected_latex = r'\pi^{e^{-1}}'
        expected_str = 'pi**exp(-1)'

        # Check if the result is displayed correctly in the console
        assert result == pi**(1/e), "Rendering of pi**(1/e) is inaccurate"

        # Check if LaTeX and str functions return the expected results
        assert latex(result) == expected_latex, "LaTeX representation is incorrect"
        assert str(result) == expected_str, "str representation is incorrect"

        print("Issue is not present.")
        exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
