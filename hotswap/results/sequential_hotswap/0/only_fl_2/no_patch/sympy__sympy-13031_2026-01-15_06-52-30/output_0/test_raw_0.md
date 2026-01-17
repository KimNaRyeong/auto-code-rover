```python
# reproducer.py
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

def run_test():
    import sympy as sy
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)
    try:
        assert sy.Matrix.hstack(M1, M2, M3, M4).shape == (0, 6), "hstack shape with all 0-row matrices does not match expected (0, 6)"

        M1 = sy.Matrix.zeros(1, 0)
        M2 = sy.Matrix.zeros(1, 1)
        M3 = sy.Matrix.zeros(1, 2)
        M4 = sy.Matrix.zeros(1, 3)
        assert sy.Matrix.hstack(M1, M2, M3, M4).shape == (1, 6), "hstack shape with non-zero-row matrices does not match expected (1, 6)"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    run_test()
```

This script addresses the described issue by first attempting operations that would highlight discrepancies in expected behavior concerning the stacking of matrices using `sympy.Matrix.hstack`. It asserts that when stacking matrices of various widths but zero rows, the resulting width should sum to the total width of individual matrices, as per the behavior observed in sympy 1.0. The script will assert the expected behavior, print a detailed stack trace when an assertion fails due to a mismatch in observed behavior, and raise an `AssertionError` to indicate the presence of an issue. If the assertions pass, indicating that the issue has been resolved or is absent, the script will complete successfully without any output, exiting with a code of 0.