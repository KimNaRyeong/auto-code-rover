Here is a standalone Python file named `reproducer.py` designed to reproduce the issue as specified. This script checks the output of `sqf_list` against the expected results and uses the provided `print_stacktrace` function to handle and display exceptions if the output is not as expected.

```python
from sympy import symbols, sqf_list

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

def test_sqf_list_consistency():
    x = symbols('x')

    # First example (where the issue is suspected)
    expr1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    result1 = sqf_list(expr1)
    expected_result1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    assert result1 == expected_result1, "First example output is not as expected."

    # Second example (working as expected)
    expr2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    result2 = sqf_list(expr2)
    expected_result2 = (1, [(x - 2, 1), (x**2 - 1, 2)])
    assert result2 == expected_result2, "Second example output is not as expected."

if __name__ == "__main__":
    try:
        test_sqf_list_consistency()
        print("All tests passed successfully.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1) from e
```

This script:

1. Imports the necessary symbols from SymPy.
2. Defines a function to print out a stack trace when an exception is caught.
3. Implements a test function `test_sqf_list_consistency` that:
   - Defines symbolic expressions for testing.
   - Calls `sqf_list` with those expressions.
   - Checks if the returned results match the expected outcomes for both scenarios presented in the issue description.
   - Asserts to trigger an `AssertionError` if the output does not match the expectation.
4. Executes the test function within a try-except block to catch `AssertionError` exceptions, print an informative stack trace using the provided function, and exits with status code `1` to indicate failure. If no exception occurs, it prints a success message and exits with status code `0`.

This script needs to be placed at the root directory of the involved project and executed with Python 3. If the issue is present, it will raise an `AssertionError`, print the stack trace with line numbers and code context, and exit with code `1`. Once the issue is fixed, the script will complete successfully without errors, printing "All tests passed successfully," and exit with code `0`.