Here's a corrected version of `reproducer.py` that specifically aims to reproduce the issue as described, checking for the unexpected modification of contour levels when they fall outside the data range. This version ensures that the script will raise an `AssertionError` if the issue is present, adhering to the requirements.

```python
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

def main():
    x = np.linspace(0, 1, 10)
    y = np.linspace(0, 1, 10)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)  # Produces data ranging between -1 and 1

    # Define contour levels that are outside the Z data range
    levels = [100]  # A level that does not exist in Z

    try:
        plt.figure()
        myplot = plt.contour(X, Y, Z, levels=levels)
        plt.close()

        # If Matplotlib overrides the specified levels, it should print the minimum data range instead
        # The issue is present if the output levels don't match the specified levels
        assert myplot.levels == levels, "Matplotlib unexpectedly modified the specified contour levels."

    except AssertionError as e:
        print("Issue Detected:")
        print_stacktrace(e)
        raise  # Reraises the error to ensure script exits with an error code if issue is present.

    except Exception as e:
        print("Unexpected Error:")
        print_stacktrace(e)
        raise  # Reraises any unexpected error.

    print("No issue detected with contour level autoscaling.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)  # Exit with error code 1 if assertion fails, indicating issue is present.
    exit(0)  # Exit with code 0, indicating the issue is fixed or not present.
```

This script will execute a contour plot using Matplotlib, intentionally setting the `levels` argument to a value that is outside the data range of `Z`. If Matplotlib modifies these specified levels to something within the data range (or to a single value such as the minimum of the data range, as described in the issue), the script will detect this by comparing `myplot.levels` with the originally specified `levels` and subsequently raise an `AssertionError`. The use of `print_stacktrace(e)` ensures that the error information is clearly presented when the issue occurs.