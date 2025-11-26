Here is the `reproducer.py` file that reproduces the issue:
```
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
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    
    try:
        assert sp.minimal_polynomial(a) == sp.minimal_polynomial(-1 + sp.sqrt(2))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script creates an algebraic number `b` and converts it to a number field using `to_number_field`. It then checks if the minimal polynomial of `a` is equal to the minimal polynomial of `-1 + sqrt(2)`, which should be the case. If not, it raises an `AssertionError` with a stack trace.

You can run this script by executing `python3 reproducer.py` in the root directory of the project. If the issue is present, it will raise an `AssertionError` and print a stack trace. If the issue is fixed, it will exit with code 0.