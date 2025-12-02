from math import pi, e
from sympy import latex
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

if __name__ == "__main__":
    try:
        result = pi**(1/e)
        expected_latex = r'\pi^{e^{-1}}'
        expected_str = 'pi**exp(-1)'

        # Check if the result is displayed incorrectly
        if result != pi**(1/e):
            raise AssertionError(f"Incorrect rendering of pi**(1/e): got {result}, expected {pi**(1/e)}")

        # Check if LaTeX and str functions return the expected results
        if latex(result) != expected_latex or str(result) != expected_str:
            raise AssertionError(f"Incorrect rendering of pi**(1/e): got {result}, expected LaTeX {expected_latex} and str {expected_str}")

    except Exception as e:
        print_stacktrace(e)
        exit(1)
