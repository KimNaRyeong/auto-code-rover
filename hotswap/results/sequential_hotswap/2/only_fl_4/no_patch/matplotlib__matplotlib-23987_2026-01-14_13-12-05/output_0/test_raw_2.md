To fulfill the requirements and aiming to specifically target the issue as described, including raising an `AssertionError` if the issue is present while aiming for an exit code of 0 when the issue is not encountered, the following Python script, named `reproducer.py`, has been designed. This script assumes the problem to be reproducible based on the UserWarning being caught when `constrained_layout=False` is explicitly set.

```python
import matplotlib.pyplot as plt
import numpy as np
import warnings
import sys

# Function to print the stack trace of an exception
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
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Catch all warnings

        # Reproducing the provided code snippet
        a = np.linspace(0, 2*np.pi, 100)
        b = np.sin(a)
        c = np.cos(a)
        fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
        ax[0].plot(a, b)
        ax[1].plot(a, c)
        plt.subplots_adjust(wspace=0)  # Expected to not raise a warning if constrained_layout=False is properly respected

        # Check if the UserWarning is in the list of caught warnings
        for warning in w:
            if issubclass(warning.category, UserWarning) and "incompatible with subplots_adjust" in str(warning.message):
                print_stacktrace(AssertionError("UserWarning triggered: " + str(warning.message)))
                exit(1)

    print("Issue not found, the script exited with code 0.")
    exit(0)

if __name__ == "__main__":
    main()
```

This script is tailored to the specific context of detecting a warning related to the constrained layout setting in Matplotlib when it's explicitly turned off (`constrained_layout=False`). The `main` function wraps the problematic code snippet within a warning capture context, specifically looks for the `UserWarning` that matches the description provided in the bug report, and then uses the `print_stacktrace` function if the issue is present to provide detailed diagnostic information before exiting with a non-zero status code (`exit(1)`). The script ends with a successful message and exits with `exit(0)` when no such warning is found, indicating the absence of the reported bug under the current test conditions.