Here is the `reproducer.py` file that reproduces the issue:
```
import matplotlib.pyplot as plt

def test_ncols_ncol_issue():
    fig, ax = plt.subplots(ncols=2)  # This should work
    try:
        ax.legend(ncols=3)  # This should raise an error
        assert False, "Expected TypeError: legend() got an unexpected keyword argument 'ncols'"
    except TypeError as e:
        print_stacktrace(e)
        assert str(e).startswith("legend() got an unexpected keyword argument 'ncols'"), "Unexpected error message"

def test_nrows_nrow_issue():
    fig, ax = plt.subplots(nrows=2)  # This should work
    try:
        ax.legend(nrows=3)  # This should raise an error
        assert False, "Expected TypeError: legend() got an unexpected keyword argument 'nrows'"
    except TypeError as e:
        print_stacktrace(e)
        assert str(e).startswith("legend() got an unexpected keyword argument 'nrows'"), "Unexpected error message"

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

if __name__ == "__main__":
    test_ncols_ncol_issue()
    test_nrows_nrow_issue()
```
This script will raise an `AssertionError` when the issue is present, and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

You can run this script using `python3 reproducer.py`.