Here is the standalone Python file `reproducer.py` to reproduce the issue:

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
    b = sp.Rational(1, -sp.sqrt(2))
    a = sp.to_number_field(b)
    if not (a.minpoly == sp.Poly([1, 0, -2], 'x')):
        raise AssertionError("Issue present")
    else:
        print("Issue fixed")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script will create the algebraic number `a` and check if its minimal polynomial is correct. If not, it raises an `AssertionError`, which is caught by the script and prints a stack trace using the provided function.