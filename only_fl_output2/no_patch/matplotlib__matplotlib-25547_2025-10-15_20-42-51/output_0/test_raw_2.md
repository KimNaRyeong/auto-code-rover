To address the requirement for a standalone Python script that raises an `AssertionError` when a given issue is present and exits with code 0 when the issue is fixed, we need to ensure correct implementation of the script including a fix for the previous error related to the incorrect usage of the context manager. This script will attempt to reproduce both issues described, one involving `UserWarning` with all-nan values and the other involving `StopIteration` with all-nan errorbars in Matplotlib.

```python
import numpy as np
import matplotlib.pyplot as plt
import warnings

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

def test_userwarning_all_nan_values():
    # This section tests if the UserWarning is thrown when it shouldn't be
    c = np.full(10, np.nan)
    plt.scatter(np.ones(10), np.ones(10), c=c)
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            plt.show()
            assert not any(issubclass(warning.category, UserWarning) for warning in w), \
                "Unexpected UserWarning thrown for all NaN values"
    finally:
        plt.close('all')

def test_stopiteration_all_nan_errorbars():
    # This section tests if the StopIteration error is raised when it shouldn't be
    fig, ax = plt.subplots(1, 1)
    try:
        ax.errorbar([0], [0], yerr=[np.nan])
    except StopIteration as e:
        print_stacktrace(e)
        raise AssertionError("StopIteration should not be raised with all NaN yerr") from None
    finally:
        plt.close('all')

if __name__ == "__main__":
    try:
        test_userwarning_all_nan_values()
        test_stopiteration_all_nan_errorbars()
        print("Tests successfully completed without any issue.")
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

### Key Changes and Fixes:
1. **Context Manager Correction for Capturing Warnings**: The `force_warning_check` function attempted previously failed because it was a factory function that did not itself serve as a context manager. In this revision, `warnings.catch_warnings(record=True)` is directly invoked within the relevant test function to correctly manage the warning state.

2. **Assertion Logic Against UserWarning**: The revised script explicitly checks for the existence of a `UserWarning` within the list of caught warnings pertaining to the operation that involves `all-nan` values, raising an AssertionError with an appropriate message if such warnings are detected.

3. **Exception Handling for `StopIteration`**: The approach to capturing the `StopIteration` exception in the error bar plotting test is maintained from the initial outline, with the addition of a finally block ensuring the clean-up of Matplotlib figures to prevent resource leaks.

4. **Execution Flow Management**: The "main" block at the end of the script executes the test functions in sequence, directly handling and reporting `AssertionError` exceptions that may arise, ensuring clarity on whether the issue is present or resolved per the script's usage instructions.

This scripting approach facilitates an accurate check for the specified issues by running it in an environment with the mentioned versions of Python and Matplotlib, ensuring straightforward replication and debugging steps based on the provided scenarios.