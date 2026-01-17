Sure, I will provide you with a Python script named `reproducer.py` that follows your specifications. The script aims to reproduce the inconsistency issue you've mentioned with `sqf` and `sqf_list` outputs. For working with polynomial expressions, I'll assume we're using `sympy`, a Python library for symbolic mathematics.

```python
import sympy as sp

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
    # Define symbol
    x = sp.symbols('x')

    # Test cases
    expr1 = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    expected_outcome1 = (1, [(x**2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])

    expr2 = x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2
    expected_outcome2 = (1, [(x - 2, 1), (x**2 - 1, 2)])

    try:
        # Test the first expression
        result1 = sp.sqf_list(expr1)
        assert result1 == expected_outcome1, "Mismatch in the first output"

        # Test the second expression
        result2 = sp.sqf_list(expr2)
        assert result2 == expected_outcome2, "Mismatch in the second output"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code
    else:
        print("All tests passed successfully.")
        exit(0)  # Exit successfully when the issue is fixed

if __name__ == "__main__":
    main()
```

This script tests the behavior of the `sqf_list` function from `sympy` with two expressions. The first part checks for the reported issue's presence, where an unexpected output might occur due to the inconsistency in handling square-free factorization (`sqf` and `sqf_list`). The second part is to test a comparison where the output is expected to be correct to ensure the script covers both scenarios.

When executed, the script will raise an `AssertionError` if the outcomes from `sympy`'s `sqf_list` function do not match the expected outputs hardcoded in the script, indicating that the issue is present. If the issue is fixed, it should print "All tests passed successfully." and exit with code 0.