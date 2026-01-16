Certainly! Below is the content for a `reproducer.py` Python script designed to reproduce the issue you've described. It attempts to demonstrate the unexpected behavior with `Subs` object substitution in the SymPy library and will raise an `AssertionError` if the issue exists, along with a detailed stack trace for better debugging.

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

def test_subs_hashing_issue():
    x, y, a, z = sp.symbols('x y a z')
    original_subs = sp.Subs(x+y, (a,), (4,))

    # Perform the substitution that should lead to an issue
    modified_subs_direct = original_subs.subs(a, z)
    
    # Creating a Subs with the same variable replaced
    modified_subs_indirect = sp.Subs(x+y, (a,), (a,)).subs(a,z)
    
    try:
        assert modified_subs_direct == modified_subs_indirect, "The hashing of substituted objects does not match"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_subs_hashing_issue()
        print("No issue detected, the script executed successfully.")
    except AssertionError:
        # An AssertionError indicates the issue is present
        print("The issue was reproduced successfully.")
```

This `reproducer.py` file first defines a function to print detailed stack traces upon catching an exception. It then proceeds to recreate the problematic scenario with symbolic expressions using SymPy. By performing substitutions in two different manners that are logically expected to yield the same result but apparently do not, we can demonstrate the described issue. When executed, the script will assert whether the issue is present by comparing the outcomes of the two substitution approaches. If the outcomes are not as expected (that is, if the results from the direct and indirect substitution processes differ), an `AssertionError` will be raised, and the stack trace of this error will be printed, helping to understand where and why the issue occurs.