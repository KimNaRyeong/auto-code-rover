Here is the reproducer script:

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

def main():
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    if str(a) != '-1 + sqrt(2)' or str(sp.minimal_polynomial(b)) != '_x**2 - 2*_x - 1':
        raise AssertionError("Issue not reproduced")
    print_stacktrace(AssertionError("Issue not fixed"))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script creates the algebraic number `b` and then calls `to_number_field` to create an `AlgebraicNumber` generating the extension field. It then checks if the sign of the generated number is positive, and if the minimal polynomial of `a` is correct. If not, it prints a stack trace and raises an `AssertionError`.