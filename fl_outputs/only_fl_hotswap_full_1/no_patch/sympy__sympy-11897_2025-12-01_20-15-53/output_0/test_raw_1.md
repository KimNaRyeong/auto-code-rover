 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import pprint, latex, var, exp, log, Rational
from sympy.abc import x, y

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    # Test case 1
    var('x', positive=True)
    latex_result = latex(exp(-x)*log(x))
    pprint_result = pprint(exp(-x)*log(x))
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

    # Test case 2
    var('x y')
    latex_result = latex(1/(x + y)/2)
    pprint_result = pprint(1/(x + y)/2)
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

    # Test case 3
    var('x y', positive=True)
    latex_result = latex(Rational(1, x + y))
    pprint_result = pprint(Rational(1, x + y))
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

if __name__ == "__main__":
    try:
        test_issue()
        print("All tests passed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace if the issue is present, or print "All tests passed." if the issue is fixed.

Note that I added a third test case to check if the assumptions affect printing, as requested in the issue description. The test case uses the `positive` assumption for both `x` and `y`, and checks if the LaTeX printer and the pretty printer give the same output for a rational expression.