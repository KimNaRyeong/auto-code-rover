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

def reproduce_issue():
    import sympy as sp
    try:
        with sp.evaluate(False):
            point = sp.S('Point2D(Integer(1),Integer(2))')
        # If we reach this point without an exception, the issue has been fixed.
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

def main():
    issue_fixed = reproduce_issue()
    assert not issue_fixed, "The issue is not reproduced. It may have been fixed."

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the reported issue by creating a `Point2D` object within a context where expressions shouldn't be automatically evaluated (`with sp.evaluate(False)`). The script will print the stack trace of the error if the issue is present.

The use of `assert not issue_fixed` is to raise an `AssertionError` if the issue is not reproduced (i.e., the code does not raise an exception). This serves as an indicator that the issue might have been fixed since no exception consistent with the issue description was thrown. Remember, this script will exit successfully with code 0 if the assertion fails due to how exceptions are handled in Python.