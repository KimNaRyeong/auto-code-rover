Certainly, below is a standalone Python file named `reproducer.py` designed to reproduce the reported issue. When run, this script will check if the problem with how instances of `Mul` containing an unevaluated addition and a fraction are represented. If the issue exists, it raises an `AssertionError` along with a stack trace. If the issue is resolved, the script will exit gracefully with code 0.

Please note that for this script to run correctly, you'll need to have the SymPy library installed in your Python environment. 

```python
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

def check_issue():
    from sympy import Mul, Rational, symbols, SympifyError

    x, y = symbols('x y')

    # Test case where the rational number is the first argument.
    case1 = Mul(Rational(1, 2), x + y, evaluate=False)
    expected_str_1 = "(x + y)/2"
    actual_str_1 = str(case1)

    # Test case where the rational number is the second argument.
    case2 = Mul(x + y, Rational(1, 2), evaluate=False)
    expected_str_2 = "(x + y)*1/2"
    actual_str_2 = str(case2)

    try:
        assert actual_str_1 == expected_str_1, "Case 1 does not match expected output."
        assert actual_str_2 == expected_str_2, "Case 2 does not match expected output."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status when the issue is present

if __name__ == "__main__":
    check_issue()
    print("No issue found.")  # This line is reached only if no issue is present.
    sys.exit(0)  # Exit normally when the issue is fixed
```

This script imports the necessary components from SymPy (`Mul`, `Rational`, `symbols`), attempts to create the problematic expressions, and then checks if their string representations match the expected outputs considering the issue. If the representations do not match (indicating the issue is present), an `AssertionError` is thrown, and the custom `print_stacktrace` function is called to display the error details.