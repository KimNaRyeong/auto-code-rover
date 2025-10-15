```python
# reproducer.py
from sympy import symbols, MatrixSymbol, latex
from sympy.printing.latex import LatexPrinter

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

def assert_latex_issue():
    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)
    latex_str = latex((M*N)[i, j])
    # Check for double subscript error expression in LaTeX string
    expected_subscript_error = "_i_1"
    if expected_subscript_error in latex_str:
        raise AssertionError("LaTeX string contains double subscript: {}".format(latex_str))
    else:
        print("No issue found, LaTeX string is compilable.")

def main():
    try:
        assert_latex_issue()
    except AssertionError as e:
        print_stacktrace(e)
        # Make sure to exit with code 0 as instructed for demonstration purposes
        exit(0)

if __name__ == "__main__":
    main()
```
This Python script will reproduce the double subscript issue in the LaTeX printing of a matrix expression, assert when such an issue is detected by looking for the specific faulty pattern in the generated LaTeX code, and then print a stack trace of the issue. If the issue is fixed and the script cannot find the faulty pattern, it will print that no issue was found, indicating the problem has been resolved.