Given the initial misunderstanding of the issue reproduction, I've reassessed the approach to correctly raise an `AssertionError` when the issue is present based on your detailed description.

Here's the corrected standalone Python script, `reproducer.py`, which is intended to closely adhere to the conditions described, thereby effectively reproducing the issue and printing a stack trace if the problem persists.

```python
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

def reproduce_issue():
    x = symbols('x')
    
    # Reproducing the unexpected behavior: RootOf might ignore the generator
    try:
        # Case where RootOf should respect the generator being tan(x)
        expr_subbed = (x**3+x-1).subs(x, tan(x))
        root_of_subbed = RootOf(expr_subbed, 0)
        # Asserting if RootOf correctly identifies the new generator as tan(x).
        # Expected failure to catch the described bug
        assert root_of_subbed.poly.gen == tan(x), "Failed: RootOf ignores the generator when it shouldn't."
    except AssertionError as e:
        print_stacktrace(e)

    # Another case where the expected generator is not observed
    try:
        root_of_direct = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
        # Attempt to directly compare generators without substituting
        # Expected failure similar to above described condition
        assert root_of_direct.poly.gen == tan(x), "Failed: RootOf does not correctly identify tan(x) as the generator."
    except AssertionError as e:
        print("AssertionError for case where generator should be tan(x) but isn't:")
        print_stacktrace(e)

if __name__ == '__main__':
    reproduce_issue()
```

This script now includes two assertions specifically designed to fail under the conditions demonstrating the issue, where `RootOf` doesn't handle the generator as expected when it encounters a substituted expression or a straightforward case that involves `tan(x)`. It uses the provided function `print_stacktrace` to clearly print the details when an assertion error occurs, indicating the issue is present. 

If the script produces an `AssertionError` and prints a stack trace, it means the issue remains unresolved. If, instead, it executes without raising an error, this would indicate the issue has been addressed in the version of SymPy being tested.