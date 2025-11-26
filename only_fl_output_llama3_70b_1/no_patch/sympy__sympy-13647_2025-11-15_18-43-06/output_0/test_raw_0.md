Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sm

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
    M = sm.eye(6)
    V = 2 * sm.ones(6, 2)
    M_col_inserted = M.col_insert(3, V)
    
    # Check if the issue is present
    expected_bottom_right_corner = sm.eye(3)
    actual_bottom_right_corner = M_col_inserted[:3, -3:]
    try:
        assert (expected_bottom_right_corner == actual_bottom_right_corner).all()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue and raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, it will exit with code 0.