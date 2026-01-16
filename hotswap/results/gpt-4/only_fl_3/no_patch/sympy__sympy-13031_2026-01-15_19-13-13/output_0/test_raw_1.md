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

    # Sympy 1.1 Change Reproduction
    M1 = sy.Matrix.zeros(0, 0)
    M2 = sy.Matrix.zeros(0, 1)
    M3 = sy.Matrix.zeros(0, 2)
    M4 = sy.Matrix.zeros(0, 3)

    try:
        result_0_row = sy.Matrix.hstack(M1, M2, M3, M4).shape
        # Expected behavior for sympy before version 1.1 would be (0, 6)
        # If the behavior change is present (sympy 1.1 and later), it will be (0, 3)
        assert result_0_row == (0, 6), f"Behavior change detected: Expected (0, 6), got {result_0_row}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with code 1 if issue is present

    # If the script has not exited by this point, the issue is not present
    print("Test passed: No issue detected.")

if __name__ == "__main__":
    run_test()
```

This script specifically tests for the behavior change between Sympy 1.0 to 1.1 regarding the `Matrix.hstack` method with matrices that have 0 rows. If the behavior change is present (i.e., the shape is `(0, 3)` indicating the issue in Sympy 1.1), it will assert an error, trigger the `print_stacktrace` method, and exit with code 1. If the behavior change is not detected (the expected result `(0, 6)` is still valid), the test will pass, printing "Test passed: No issue detected." and exit normally with code 0.