```python
# reproducer.py
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

def main():
    from sympy import MatrixSymbol, latex

    # Define matrix symbols
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)

    # Substitute y with -y in the matrix product
    expr = (x*y).subs(y, -y)
    
    # Generate LaTeX representation
    latex_str = latex(expr)
    
    # We expect the LaTeX output to have parentheses around "-y"
    expected_latex = "x \\left(- y\\right)"
    
    # Checking if the issue is present
    try:
        assert latex_str == expected_latex, f"Expected LaTeX output: '{expected_latex}', but got '{latex_str}'"
        print("Issue seems to be fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        # Exit with code 0 to indicate the script worked as expected (to reproduce the issue)
        import sys
        sys.exit(0)
```

This script checks whether the issue described is present in the `sympy` package's LaTeX printer functionality. The `main` function defines two matrix symbols `x` and `y`, substitutes `y` with `-y` in the product `x*y`, and then compares the LaTeX representation of the expression with the expected result that includes parentheses around `-y`. If the actual and expected LaTeX strings do not match, indicating the issue is present, it raises an `AssertionError`. The script ensures a non-zero exit code only if an unexpected error occurs, thereby indicating successful issue reproduction (or its presence) with a zero exit code.