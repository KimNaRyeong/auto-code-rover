Given the specific instructions and the goals to achieve with this script, let's create a Python script that adheres to the guidelines provided. This script will attempt to replicate the issue as described. It's worth mentioning that whether or not the `AssertionError` is reproduced might depend on the version of Matplotlib used and how it has been built (e.g., with or without assertions enabled). If the matplotlib package has been fixed regarding this issue or if assertions are disabled, the script might not be able to reproduce the error and exit with code 0, indicating the absence of the issue.

Here's the Python script:

```python
# reproducer.py
import matplotlib.pyplot as plt
import numpy as np
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_contour_with_all_nans():
    x = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    plt.contour(x)

def main():
    try:
        test_contour_with_all_nans()
    except AssertionError as e:
        print("AssertionError was raised as expected:", file=sys.stderr)
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate failure/reproduction of the issue.
    except Exception as e:
        print("An unexpected exception occurred:", file=sys.stderr)
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate an unexpected error occurred.
    else:
        print("No AssertionError raised, the issue did not occur or has been fixed.")
        exit(0)  # Exit with zero to indicate the issue did not reproduce / has been fixed.

if __name__ == "__main__":
    main()
```

The above script is a simple, executable Python file intended to reproduce the specific `AssertionError` when plotting a contour with an all-NaN array using Matplotlib, under the conditions that would trigger such an error. The script tries to run the operation that is expected to fail, catching and handling the exception to provide a traceback if the failure occurs as described in the issue report.

If the issue is present, it will raise an `AssertionError`, and the script will print a detailed stack trace and exit with code 1. If the issue is not reproduced (e.g., due to a fix in Matplotlib or assertions are disabled in the build being used), it will exit gracefully with code 0, indicating the absence of the problem.