```python
# reproducer.py
import matplotlib.pyplot as plt
import numpy as np
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

def test_constrained_layout_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Turn all warnings into catch-able warnings

        # Code that triggers the warning
        a = np.linspace(0, 2*np.pi, 100)
        b = np.sin(a)
        c = np.cos(a)
        fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
        ax[0].plot(a, b)
        ax[1].plot(a, c)
        plt.subplots_adjust(wspace=0)

        # Check if the specific warning was raised
        found_specific_warning = any("constrained_layout" in str(warn.message) and "subplots_adjust" in str(warn.message) for warn in w)
        if found_specific_warning:
            raise AssertionError("Constrained layout UserWarning triggered even when constrained_layout is set to False.")

if __name__ == "__main__":
    try:
        test_constrained_layout_warning()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error if the issue is present
    print("No issue found.")
    exit(0)  # Exit with success if the issue is fixed
```