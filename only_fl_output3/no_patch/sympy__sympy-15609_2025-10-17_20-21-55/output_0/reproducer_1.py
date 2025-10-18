from sympy import symbols, MatrixSymbol, latex
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

def check_latex_compilable():
    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)
    latex_str = latex((M*N)[i, j])

    # The issue was inaccurately checked in the previous script.
    # The correct condition to raise an AssertionError based on the described scenario:
    expected_issue_part = "_{_"
    if expected_issue_part in latex_str:
        raise AssertionError("Detected double subscript in LaTeX string, which is not compilable. Latex output: " + latex_str)

if __name__ == "__main__":
    try:
        check_latex_compilable()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with non-zero to indicate failure
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Catching any other unexpected issue
    print("No issue detected, exiting with code 0.")
    sys.exit(0)
