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
    try:
        expected_str_output = "A - A*B - B"
        str_output = str(A - A*B - B)
        assert expected_str_output == str_output, f"str printer output is incorrect: expected {expected_str_output}, got {str_output}"

        expected_pprint_output = "Matrix([[A, 0], [0, A]])"
        pprint_output = pprint(A - A*B - B)
        assert expected_pprint_output == pprint_output, f"pprint printer output is incorrect: expected {expected_pprint_output}, got {pprint_output}"

        expected_latex_output = "\\left[\\begin{matrix}A & 0 \\\\0 & A\\end{matrix}\\right]"
        latex_output = latex(A - A*B - B)
        assert expected_latex_output == latex_output, f"latex printer output is incorrect: expected {expected_latex_output}, got {latex_output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
