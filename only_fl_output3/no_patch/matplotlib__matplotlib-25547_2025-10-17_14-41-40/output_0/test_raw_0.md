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

def main():
    import matplotlib.pyplot as plt
    import numpy as np

    # Reproduce "converting a masked element to nan" UserWarning
    try:
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Did not expect an exception for only NaN colors.")

    # Reproduce "StopIteration" exception with ax.errorbar
    try:
        fig, ax = plt.subplots(1, 1)
        ax.errorbar([0], [0], yerr=[np.nan])
        plt.show()
    except StopIteration as e:
        print_stacktrace(e)
        raise AssertionError("ax.errorbar should not raise StopIteration for all NaN yerr.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Unexpected exception occurred.")

    # Exit gracefully if both cases pass without errors
    print("All tests passed successfully.")

if __name__ == "__main__":
    main()
```

Ensure you have the correct environment set up with the versions of Matplotlib (and its dependencies) that exhibit the behaviors mentioned in the bug reports. This script tries to replicate the two distinct issues: one with Matplotlib throwing a `UserWarning` when all color values are `np.nan`, and the other issue occurring in `ax.errorbar` method with `StopIteration` when `yerr` contains only `NaN` values. 

The script is intended to:
- **Fail** (and print a stack trace) when encountering the described issues.
- **Pass** (printing "All tests passed successfully.") when the issues are not present, e.g., they have been fixed in a newer release of Matplotlib.

Run this script from the root directory of your project or adjust the script's file paths as necessary to ensure it executes correctly.