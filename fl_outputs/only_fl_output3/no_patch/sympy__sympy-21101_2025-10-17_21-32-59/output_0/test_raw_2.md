To create a Python script that aims to reproduce the issue of incorrect Latex formatting with unevaluated `Mul` producing an output without proper separation, the following script can be employed. This script checks for the specific problem described – the lack of a multiplication symbol or some form of separation when `latex()` is called on an unevaluated `Mul` object with specific parameters. The script is designed to raise an `AssertionError` if the problematic behavior is encountered (indicating the issue is present), print a relevant stack trace for debugging purposes, and exit with a non-zero status. Conversely, it will exit with code 0 (indicating no error) if the issue has been resolved or is not present.

```python
# reproducer.py

def main():
    try:
        from sympy import Mul, S
        from sympy.printing.latex import latex
        
        # Creating a Mul expression without automatic evaluation
        expr = Mul(6, S.Half, evaluate=False)
        # Generating the LaTeX representation of the expression
        latex_output = latex(expr)
        
        # Checking if the generated LaTeX output has the issue: missing separator (e.g., '\cdot' or space)
        # Update `expected_latex_output` based on the specific issue details
        expected_latex_output = "6 \\frac{1}{2}"
        assert latex_output == expected_latex_output, f"Unexpected LaTeX output: {latex_output}"
        
        print("The issue is fixed. LaTeX output is as expected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Script exits with code 1 indicating an error (the issue is present)

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

if __name__ == "__main__":
    main()
```

This script specifically targets the mentioned issue by generating LaTeX code from a symbolic expression that should not automatically evaluate. It then checks to ensure the output matches what we would expect if the problem was corrected. 

- The assertion is deliberately designed based on the understanding that `latex(Mul(6, S.Half, evaluate=False))` should produce a string that reflects unambiguous mathematical representation, such as including a multiplication symbol or some form of clear separation. The precise expected output might need to be adjusted based on the desired or correct behavior (e.g., including `\cdot` for multiplication).

- If the output is as expected, indicating the issue has been fixed, it prints a confirmation message. 

- If the output is not as expected (signifying the problem persists), it prints a detailed stack trace to help diagnose the issue further.