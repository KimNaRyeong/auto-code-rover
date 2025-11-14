```python
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

def test_issue():
    from sympy import Symbol, MatrixSymbol, MatAdd

    # Issue setup
    A = MatrixSymbol('A', 2, 2)

    # Attempt to reproduce the issue
    try:
        result = MatAdd(A, A, evaluate=True)
        # Check if the issue exists
        assert str(result) != "2*A", "Issue not fixed"
    
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Re-raise the exception to ensure the script exits appropriately

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError:
        # This means the test has failed i.e., the issue still exists
        exit(1)  # Non-zero exit code to indicate failure
    else:
        print("No issue found or the issue has been fixed.")
        exit(0)  # Exit code 0 to indicate success/no issue
```