Certainly! Below is the `reproducer.py` script designed to address both issues you reported. This script attempts to recreate the issues with `matplotlib` as described, and checks if the warnings and errors are triggered accordingly. Note, however, that handling warnings and errors in Python can be somewhat version-dependent, and the below script is intended for use with Python 3 environments where `matplotlib` and `numpy` are installed.

```python
import numpy as np
import matplotlib.pyplot as plt
import warnings
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


def main():
    # Test for the issue with UserWarning when all values are "bad" (np.nan)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()
        # Expecting UserWarning to be present
        assert any(isinstance(warning.message, UserWarning) for warning in w), "Issue 1: Warning not raised for all NaN values."

    # Test for the issue with StopIteration when yerr contains only NaN values
    try:
        fig, ax = plt.subplots(1, 1)
        ax.errorbar([0], [0], yerr=[np.nan])  # This should not raise StopIteration
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue 2: Exception raised for all NaN values in yerr."

    print("Both issues reproduced successfully (assuming correct AssertionError).")


if __name__ == "__main__":
    main()
```

This script is structured to perform two tests: First, it recreates the scenario where a `UserWarning` is expected due to all values being `np.nan` and asserts that such a warning is indeed raised. Second, it recreates the scenario described for `ax.errorbar` where an all `np.nan` `yerr` parameter leads to a crash, specifically looking for a `StopIteration` exception to ascertain if the bug is present.

Before running the script, ensure you have a suitable Python environments setup with `numpy` and `matplotlib` installed. The expected behavior is:

- If the issues are present, you should see an AssertionError for the first check and a printed stack trace for the second.
- If the issues have been fixed in a newer version of `matplotlib` than what was reported, the script should complete without errors, demonstrating that the issues have been addressed.