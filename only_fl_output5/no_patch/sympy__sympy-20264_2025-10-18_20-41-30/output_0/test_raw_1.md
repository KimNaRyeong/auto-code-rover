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

def test_recursion_issue():
    from sympy import Pow, Rational, latex
    # Attempt to replicate the issue with specific Pow and Rational inputs
    try:
        latex(Pow(Rational(1,2),-1, evaluate=False))
        # No exception means the issue is likely fixed
        return False
    except RecursionError as e:
        # RecursionError occurred, issue is present.
        print_stacktrace(e)
        return True
    except Exception as e:
        # Unexpected exception type, could indicate other problems.
        print(f"Unexpected error encountered: {e}")
        return False

def main():
    issue_present = test_recursion_issue()
    if not issue_present:
        print("No RecursionError, issue might be fixed or not reproduced.")
        exit(0)  # Exit code 0 for success.
    else:
        raise AssertionError("RecursionError issue reproduced successfully.")

if __name__ == "__main__":
    main()
```

This code snippet is intended to be saved as `reproducer.py` and executed in the root directory of a project that uses the `sympy` library. The purpose of this script is to check whether a specific issue, a `RecursionError` that occurs under certain conditions when converting a `sympy` `Pow` object with `Rational` arguments to LaTeX format, still exists. The `print_stacktrace` function is used to provide detailed traceback information if the error occurs. If the issue has been fixed, the script will complete normally and exit with code 0, indicating success. If the issue is still present, an `AssertionError` will be raised, indicating failure to fix the issue.