# reproducer.py
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

def check_idx_bounds_accepts_non_integer():
    try:
        m, n = sp.symbols("m, n", real=True)
        i = sp.Idx("i", (m, n))  # This line should raise a TypeError
        # If the TypeError was not raised, then the issue is present
        raise AssertionError("Idx object accepted non-integer bounds without raising an error.")
    except TypeError as e:
        print("The issue has been fixed.")
        return
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    check_idx_bounds_accepts_non_integer()
