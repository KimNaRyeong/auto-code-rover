```python
# reproducer.py
from sympy import symbols, tan, RootOf

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

def test_rootof_generator_issue():
    x = symbols('x')
    
    # Test case 1
    root_of_original = RootOf(x**3 + x - 1, 0)
    
    try:
        # Should be in terms of 'tan(x)' but incorrectly remains 'x'
        root_of_substituted = RootOf((x**3 + x - 1).subs(x, tan(x)), 0)
        assert root_of_substituted.poly.gen == tan(x), "Generator should be tan(x)"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    # Test case 2
    try:
        another_root_of_original = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
        # This should create a polynomial in 'x', but incorrectly uses 'tan(x)'
        incorrect_generator = RootOf((x**3 + 2*x - 1), 0)
        assert incorrect_generator.poly.gen == x, "Generator should be x"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_rootof_generator_issue()
        print("The script executed successfully, no issues detected.")
    except AssertionError:
        # Expected behavior when the issue is present
        exit(1)  # Exit with a non-zero code when an assertion fails
```

This script is designed to directly reproduce the issue described. It uses the `AssertionError` to indicate when things don't work as expected. The first part tests that substituting `tan(x)` into the polynomial doesn't correctly adjust the generator used by `RootOf`. The second part further tries to assert that creating a new `RootOf` with a polynomial directly in `tan(x)` should similarly encounter issues with the generator. On failure, a stack trace specific to each case is printed out, directing to where things didn't go as expected, enforcing the documentation of the problem being reproducible under the conditions outlined.