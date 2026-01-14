Here's a `reproducer.py` script that will check for the described issue regarding the `Idx` object in SymPy. The script attempts to create an `Idx` instance with symbol bounds. If it incorrectly accepts these non-integer bounds without raising an error, the script will print the expected stack trace; otherwise, it will exit quietly if the issue is fixed (i.e., it raises a `TypeError`).

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

def test_idx_with_non_integer_bounds():
    try:
        m, n = sp.symbols("m, n", real=True)
        _ = sp.Idx("i", (m, n))
    except TypeError as e:
        # If a TypeError is raised, then it's likely the issue has been fixed
        # Exiting with code 0 as the issue is considered fixed if TypeError is raised
        print("The issue is fixed.")
        exit(0)
    except Exception as e:
        # For any other exceptions, let's print the stacktrace
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.")
    else:
        # If no exception is raised, then the issue is still present
        raise AssertionError("Idx object incorrectly accepts non-integer bounds.")

if __name__ == "__main__":
    test_idx_with_non_integer_bounds()
```

This script tests specifically for the issue where the `Idx` class incorrectly accepts non-integer bounds without raising an error. It assumes this behavior is incorrect according to the issue description provided.