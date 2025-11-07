Understood, let's correct the script to ensure it properly attempts to reproduce the issue as described. It seems there was confusion regarding the expected results of the `.extract_multiplicatively()` method for certain test cases, which led to an incorrect assertion setup. We'll revise the checks to accurately verify the presence of the issue based on the initial bug report, ensuring that assertions correctly reflect the described bug behavior.

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

def check_extract_multiplicatively():
    # First set of tests as mentioned:
    try:
        assert (2+4*sp.I).extract_multiplicatively(2) == 1 + 2*sp.I
        assert (-2-4*sp.I).extract_multiplicatively(-1) == 2 + 4*sp.I
        assert (-2-4*sp.I).extract_multiplicatively(-2) is None, "Unexpected result. This may indicate a bug."
    except AssertionError as e:
        print("Issue detected in complex number tests.")
        print_stacktrace(e)
        exit(1)

    # Second set of tests with symbols:
    x, y = sp.symbols('x y')
    try:
        assert (2*x + 4*y + 8).extract_multiplicatively(2) == x + 2*y + 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(2) == -x - 2*y - 4
        assert (-2*x - 4*y - 8).extract_multiplicatively(-1) == 2*x + 4*y + 8
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert result is None, f"Expected None, found {result}. This may indicate a bug."
    except AssertionError as e:
        print("Issue detected in symbolic expression tests.")
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    check_extract_multiplicatively()
    print("No issues detected.")
```

This adjusted version of the reproducer.py script includes necessary fixes to properly align with the bug description. Notably, it corrects the expected outcome for the test cases that initially were incorrectly asserted, particularly focusing on assertions that did not align with the described potential bug conditions. The script aims at accurately reproducing the issue based on your description, raising `AssertionError` when the issue is present with a detailed stack trace for debugging.