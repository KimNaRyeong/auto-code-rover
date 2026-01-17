Based on the requirements to reproduce the issue accurately, here's a standalone Python script suitable for your project structure and execution method. This script is designed to explicitly target the described issue with the `.apart()` function in `sympy` version `1.0`. If the issue persists, `AssertionError` will be raised, otherwise, the script will exit with code 0 indicating the issue is resolved.

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

def main():
    from sympy import symbols, sympify

    # Defining the symbols
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)

    # The given expression
    bug_expression = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

    # Perform the substitution and call to apart() as per the issue description
    result_after_subs_and_apart = bug_expression.subs(a, 1).apart(t)

    # Direct call to apart() on the original bug_expression
    result_direct_apart = bug_expression.apart(t)

    # The incorrect output observed
    incorrect_output_sympified = sympify('-a*t')

    # Check if the direct apart() call on the original bug_expression equals the incorrect result
    # And check the correctness after substitution and apart() call as per the description
    try:
        assert result_direct_apart != incorrect_output_sympified, "The issue with apart() seems to be fixed."
        assert result_after_subs_and_apart == result_direct_apart.subs(a, 1), "Inconsistent results between substitution then apart and direct apart."
        print("No issue detected, the results are consistent.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1) from e

if __name__ == "__main__":
    main()
```

This script:

- Reproduces the specific conditions and steps outlined in your issue description.
- Uses `sympify` to ensure the expression comparison accounts for the abstract syntax tree (AST) of the expressions rather than simple string comparison.
- Includes the given `print_stacktrace` function to clearly show where and why any assertion fails, offering insightful tracebacks aligned with your requirements.
- Raises an `AssertionError` with a detailed message if the issue is still present or if there's inconsistency between different methods of applying `apart()`.