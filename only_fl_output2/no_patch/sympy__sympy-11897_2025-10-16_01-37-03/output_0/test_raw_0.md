```python
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

def check_latex_vs_pretty_output(sym_expression, expected_latex, expected_pretty):
    from sympy import latex, pprint
    from io import StringIO
    import sys

    # Capture the output of the pretty printer
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    pprint(sym_expression)
    sys.stdout = old_stdout
    pretty_output = result.getvalue()

    # Generate LaTeX output
    latex_output = latex(sym_expression)

    # Check consistency between the expected and generated outputs
    assert latex_output == expected_latex, "LaTeX output inconsistency detected"
    assert pretty_output.strip() == expected_pretty, "Pretty output inconsistency detected"

def main():
    from sympy import var, exp, log
    try:
        # Case 1
        x = var('x', positive=True)
        check_latex_vs_pretty_output(
            exp(-x)*log(x),
            '\\frac{1}{e^{x}} \\log{\\left (x \\right )}', # expected LaTeX
            '-x\nℯ  ⋅log(x)' # expected pretty
        )

        # Case 2 without assumptions affecting the print
        x, y = var('x y')
        check_latex_vs_pretty_output(
            1/(x + y)/2,
            '\\frac{1}{2 x + 2 y}', # expected LaTeX
            '    1\n─────────\n2⋅(x + y)' # expected pretty
        )

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No inconsistencies detected.")

if __name__ == "__main__":
    main()
```

This script checks for the specific inconsistencies between the LaTeX and pretty printers as described in the given issue. It raises an `AssertionError` if the issue is detected, printing a detailed stack trace using the defined `print_stacktrace` function. If the outputs are consistent with the expectations, it ends successfully with no error message.