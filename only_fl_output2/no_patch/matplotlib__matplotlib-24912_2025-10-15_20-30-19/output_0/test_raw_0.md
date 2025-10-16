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

def reproduce_issue():
    # Generate sample data
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = 50 * np.cos(X*10)*np.sin(Y*10)  # Data range mostly within 0 to 50
    
    # Attempt to plot contours with levels outside data range
    try:
        plt.figure()
        contour_plot = plt.contour(X, Y, Z, levels=[100])
        actual_levels = contour_plot.levels

        # Check if the actual levels match the requested levels
        assert actual_levels.tolist() == [100], "Contour levels were unexpectedly modified."
        plt.close()

    except AssertionError as e:
        print("Issue Detected:")
        print_stacktrace(e)
        raise  # This will raise the AssertionError to ensure exit code is not 0

    except Exception as e:
        print("Unexpected error:")
        print_stacktrace(e)
        raise  # Re-raise the unexpected exception

    print("Issue Not Detected. The script exited successfully.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError:
        exit(1)  # Exit with code 1 to indicate the issue is present
    exit(0)  # Exit with code 0 to indicate no issue was detected
```