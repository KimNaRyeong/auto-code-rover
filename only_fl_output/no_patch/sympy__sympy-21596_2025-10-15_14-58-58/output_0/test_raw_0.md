Certainly! To accomplish this task, we need a Python script that demonstrates the issue by following the provided details. The script will check the condition described in the bug report and use the `print_stacktrace` function to raise an `AssertionError` if the bug is present.

Here is how you might write such a script named `reproducer.py`:

```python
from sympy import symbols, I, Lambda, imageset, S
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
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    assert 2 not in S1, "2 should not be in S1 as per the issue description"

    # The problematic part according to the issue
    assert 2 not in S1.intersect(S.Reals), "2 being in S1.intersect(Reals) is incorrect"

    # Correct behavior final check
    S2 = S.Reals
    result = S1.intersect(S2)
    assert result == S.EmptySet, "Intersection of S1 and Reals should result in {-1, 1}, but it's showing as empty"

if __name__ == "__main__":
    try:
        check_issue()
        print("Issue is fixed or cannot be reproduced.")
        sys.exit(0)
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)
```

This script imports necessary components from SymPy, particularly for handling symbolic mathematics and sets. Then, it defines a function intended to print a stack trace of an exception in a clear format. The `check_issue` function demonstrates the problem by asserting conditions that should normally pass if the bug was not present. When the conditions related to the bug fail, an `AssertionError` is raised, which when caught, calls `print_stacktrace` to print a detailed error log that includes the file name, line number, and the snippet of code where the error occurred. 

The script exits with code 0 if the issue is fixed, indicating the absence of errors during execution. Conversely, it exits with code 1 if the issue is still present, signifying an error condition.