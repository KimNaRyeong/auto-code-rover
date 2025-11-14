Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy import FiniteSet, Interval

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
    x, y = sp.symbols('x y')
    a = FiniteSet(x, y, 2)
    b = Interval(-10, 10)
    result = str(sp.Complement(a, b))
    expected_result = '{x, y} ∩ [-10, 10]'
    try:
        assert result == expected_result
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue and raise an `AssertionError` with a stack trace when the issue is present. If the issue is fixed, the script will exit with code 0.