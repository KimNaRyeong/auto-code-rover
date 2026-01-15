To create a `reproducer.py` file that adheres to your request, we can follow these steps:

1. Import required modules: `sympy` for mathematical operations and symbol definitions, and custom error handling functions.
2. Use `sympy.printing.mathml` to generate MathML for specific functions (`acoth`, `acsc`, `asec`).
3. Check the output against what's expected. If the actual output does not match the expected output, raise an `AssertionError`.
4. Include the `print_stacktrace` function to output detailed error information.

Below is the Python script encapsulating the described logic:

```python
import sympy
from sympy.abc import x

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

def check_mathml_output():
    expected_outputs = {
        "acoth": '<apply><arccoth/><ci>x</ci></apply>',
        "acsc": '<apply><arccsc/><ci>x</ci></apply>',
        "asec": '<apply><arcsec/><ci>x</ci></apply>'
    }

    actual_outputs = {
        "acoth": sympy.printing.mathml(sympy.acoth(x)),
        "acsc": sympy.printing.mathml(sympy.acsc(x)),
        "asec": sympy.printing.mathml(sympy.asec(x))
    }

    for func, expected_output in expected_outputs.items():
        actual_output = actual_outputs[func]
        try:
            assert actual_output == expected_output, f"{func} output mismatch"
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with non-zero status code to indicate error

if __name__ == "__main__":
    check_mathml_output()
    print("No issues found.")
    exit(0)  # Exit with code 0 to indicate success
```

This script checks the MathML string output for the `acoth`, `acsc`, and `asec` functions from the Sympy library against the expected correct values. If the output does not match the expected value, an `AssertionError` is raised, and the `print_stacktrace` function prints detailed error information to standard error. If no issues are found, the script prints "No issues found." and exits with code 0, indicating success.