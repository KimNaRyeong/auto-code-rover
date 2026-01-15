Certainly, to create a Python script named `reproducer.py` that reproduces the mentioned issue with LaTeX printing for Matrix Expressions in SymPy, follow the structure provided below. This script checks if the issue exists by comparing the generated LaTeX string with the expected result, it raises an `AssertionError` if the issue persists, and uses the provided function to print a detailed stack trace.

```python
from sympy import MatrixSymbol, trace, latex

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
    n = 3  # Assume a value for n, since n is not defined in the example
    A = MatrixSymbol("A", n, n)
    expected_latex = r'\operatorname{trace}\left(A^{2}\right)'  # Assuming the expected correct LaTeX output
    generated_latex = latex(trace(A**2))

    try:
        assert generated_latex == expected_latex, "LaTeX generation for matrix expression is incorrect"
        print("Issue fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate error

if __name__ == "__main__":
    main()
```

In this script, the `main` function sets up a simple test case to generate the LaTeX representation of the square of a matrix symbol and its trace. It compares this output against the expected LaTeX string. If the output does not match the expectation (indicating the issue is present), an `AssertionError` is raised, and the stack trace is printed to help diagnose the issue. If the conditions specified are met (meaning the `assert` statement passes), it indicates that the issue has been resolved, and the script exits normally with code 0.