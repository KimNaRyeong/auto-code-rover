import sys
import traceback

from sympy import *

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
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    difference = A - A*B - B

    expected_str_output = "A - A*B - B"
    expected_pretty_output = "A - A*B - B"
    expected_latex_output = "A - A B - B"

    actual_str_output = str(difference)
    actual_pretty_output = pprint(difference)
    actual_latex_output = latex(difference)

    assert actual_str_output == expected_str_output, "The str printer does not print the difference of MatrixSymbols as expected."
    assert actual_pretty_output == expected_pretty_output, "The pretty printer does not print the difference of MatrixSymbols as expected."
    assert actual_latex_output == expected_latex_output, "The latex printer does not print the difference of MatrixSymbols as expected."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
