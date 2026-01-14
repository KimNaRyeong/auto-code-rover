To create a Python script that reproduces the reported issue and exhibits the expected behavior, you can use the following template. This script will attempt to evaluate expressions given and check if the output matches the expected results. If the evaluation does not behave as expected, it will raise an `AssertionError` and print a detailed stack trace of the issue.

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

def test_substitution_issue():
    from sympy import symbols, cos, exp, oo

    x = symbols('x')
    expr1 = x + cos(x)
    expr2 = exp(x) + cos(x)

    result1 = expr1.subs(x, oo)
    result2 = expr2.subs(x, oo)
    
    try:
        assert result1 == oo, "First expression does not evaluate to oo"
        assert result2.is_infinite, "Second expression does not evaluate to an infinite bound"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_substitution_issue()
        print("All checks passed!")
    except AssertionError:
        # If an AssertionError is caught, exit with a non-zero status code to indicate failure
        import sys
        sys.exit(1)
```

This script checks that `(x + cos(x)).subs(x, oo)` evaluates to `oo`, which is the expected behavior, and that `(exp(x) + cos(x)).subs(x, oo)` evaluates to an object representing an infinite amount or boundary. The script will raise an `AssertionError` if either of these conditions is not met, indicating that the issue still exists. If the issue is resolved, it simply prints "All checks passed!" and exits with code 0.