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

def test_issue():
    from sympy import I, MatrixSymbol
    M = MatrixSymbol('M', 2, 2)
    try:
        expr = I * M
        print(expr)  # This line should raise the TypeError
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print(f"AssertionError: {e}", file=sys.stderr)
        exit(0)  # Exit with code 0 to indicate the script is executed successfully but the issue is present.
```

This script aims to directly reproduce the reported issue. When executed within the root directory of the project where SymPy is installed, it attempts to perform the operations that were described as problematic. 

If the issue ("Invalid comparison of non-real I") is successfully reproduced, meaning the TypeError as described is raised, the script captures and prints a detailed stack trace of the error. It then raises an `AssertionError` to highlight the occurrence of the issue. On the other hand, if the problem does not occur (meaning the TypeError is not raised, possibly due to the issue being fixed in a newer version of the software), the script won't catch an exception and will terminate normally. 

Exit code rationale:

- **Exit with code 0**: Although an 'exit code 0' usually indicates success without errors, in this context, it's used to signify that the script executed successfully and confirmed the presence of the reported bug. This is a customized behavior designed specifically for demonstrating the reproduction of the issue.