```python
# reproducer.py
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def custom_min(x):
    import numpy as np
    return float(np.asarray(x).min())

def main():
    try:
        import seaborn as sns
        tips = sns.load_dataset("tips")
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except TypeError as e:
        # The specific issue we're looking for.
        print_stacktrace(e)
    except Exception as e:
        # Any other exceptions will be treated as a failure to reproduce.
        print_stacktrace(e)
        raise AssertionError("The script failed due to an unexpected exception.")

if __name__ == "__main__":
    main()
```

This script is designed to reproduce an issue related to the `seaborn.pointplot` function raising an exception when a custom estimator is used, as described in your issue report. 

When executed, it should detect whether the specific `TypeError` associated with the regression introduced in `seaborn 0.12.0.dev0` is present. 

- If the `TypeError` is caught, indicating the issue is present, the traceback of the exception is printed, following your instructions for how to display the stack trace clearly.
- If any other exception is caught, it prints the stack trace and raises an `AssertionError` saying the test failed due to an unexpected exception. This behavior ensures that the test specifically identifies the anticipated `TypeError` and does not falsely report a success for other kinds of errors.
- The `import numpy as np` statement was moved inside the `custom_min` function to ensure it's clear which operation may be raising the exception, and `import seaborn as sns` is inside the `main` function to keep the script organization logical and compact.

Please ensure all necessary libraries (`seaborn` and `numpy`, and also `matplotlib` as an indirect dependency of `seaborn`) are installed in your Python environment before running this script.