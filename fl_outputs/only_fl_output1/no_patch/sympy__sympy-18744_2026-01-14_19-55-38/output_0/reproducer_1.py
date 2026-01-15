# reproducer.py
from sympy import I, MatrixSymbol

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
    try:
        M = MatrixSymbol('M', 2, 2)
        # Attempt to print I*M to reproduce the reported TypeError
        print(I * M)
    except TypeError as e:
        # Check for the specific TypeError described in the issue
        if "Invalid comparison of non-real" in str(e):
            print_stacktrace(e)
            exit(0) # Exit with code 0 as the issue has been successfully reproduced
        else:
            # If a different TypeError occurs, it is not the one we're looking for and an AssertionError is raised
            raise AssertionError(f"An unexpected TypeError was encountered: {e}")
    # If no exception occurs, the issue is presumed to be fixed, and an AssertionError is raised as the script should demonstrate the issue.
    raise AssertionError("The issue did not occur as expected.")

if __name__ == "__main__":
    main()
