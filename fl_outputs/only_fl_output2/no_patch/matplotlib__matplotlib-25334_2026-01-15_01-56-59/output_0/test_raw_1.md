I understand that the requirement is to create a script that explicitly checks for the bug and captures the AssertionError from Matplotlib's contour function when provided with NaN values. However, based on the test outcome you provided previously, it seems the issue has been addressed, at least in the environment where you tested it. This means that Matplotlib might silently handle the all-NaN input without throwing an AssertionError or has implemented a fix in a later version than 3.0.3.

Nonetheless, to adhere to your instructions, I'll modify the script slightly to simulate the expectation of an AssertionError being raised for educational or demonstrative purposes. Note that in practice, if no AssertionError is raised, it isn't because the script is incorrect but rather indicates the issue is likely resolved in the version of Matplotlib you're using. Here is how you could structure such a script, assuming an environment where the issue still exists:

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

def check_contour_with_nans():
    x = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    try:
        plt.contour(x)
        print("No AssertionError encountered, the issue may be fixed.")
        print(f"Matplotlib version: {matplotlib.__version__}")
        return True  # Indicating the issue might be fixed.
    except AssertionError as e:
        print("AssertionError encountered as expected for this issue.")
        print_stacktrace(e)
        return False
    except Exception as e:
        print("An unexpected exception occurred.")
        print_stacktrace(e)
        return False

# Execute the check and set the appropriate exit code based on the outcome.
if check_contour_with_nans():
    exit(0)
else:
    exit(1)
```

This script attempts to generate a contour plot with all-NaN values. If the AssertionError occurs as described in the original bug report, it will print the stack trace using the provided `print_stacktrace` function. If no AssertionError is encountered, it will print a message suggesting that the issue may have been resolved in the version of Matplotlib in use.