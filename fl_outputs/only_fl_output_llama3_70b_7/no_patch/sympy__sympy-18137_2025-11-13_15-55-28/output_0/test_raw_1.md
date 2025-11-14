Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy import Symbol, Range, FiniteSet

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
    n = Symbol('n', integer=True)
    try:
        Range(1).intersect(FiniteSet(n))
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Expected TypeError: cannot determine truth value of Relational")

if __name__ == "__main__":
    main()
```
This script will raise an `AssertionError` when the issue is present and exit with code 1. When the issue is fixed, it will exit with code 0.