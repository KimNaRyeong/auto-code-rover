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
    import numpy as np
    import matplotlib.pyplot as plt

    # Attempt to reproduce the issue reported
    try:
        samples = np.random.normal(size=1000)
        x = np.linspace(-5, 5, 1000)
        fig, ax = plt.subplots()
        ax.hist(samples, log=True, density=True)
        ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi))
        fig.savefig('log.pdf')

        # Capture the figure's y-axis limits before and after the scale change
        y_limits_log = ax.get_ylim()
        ax.set_yscale('linear')
        y_limits_linear = ax.get_ylim()

        # Save the plot after changing the y_scale to linear
        fig.savefig('lin.pdf')

        # Assert to catch the disappearance issue
        # Checks if the plotted line disappears by comparing y-limits before and after scale change
        assert y_limits_log != y_limits_linear, "Y-axis limits should not be equal after changing scale."
    
    except AssertionError as e:
        # Print the stack trace when the issue is present
        print_stacktrace(e)
        raise e
    
    except Exception as e:
        # Print any other unexpected exception's stack trace
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        main()
        print("Success: No issue detected")
    except AssertionError:
        # Exit with a non-zero code if the issue is present
        exit(1)
    except Exception:
        # For unexpected errors, exit with a different non-zero code
        exit(2)
```

This script is designed to reproduce the reported issue by following these steps:
1. It generates and plots a histogram and a line plot with `log` scale.
2. It saves the plot to 'log.pdf'.
3. Then, it changes the y-axis scale to `linear` and saves the plot again to 'lin.pdf'.
4. The script uses an `assert` statement to verify if the change in y-scale effectively results in a visual change in the plot. Specifically, it compares the y-axis limits before and after the scale change to ensure they are different, indicating that the line plot does not disappear or behave unexpectedly.
5. If the line plot disappears or if the y-axis limits comparison does not behave as expected (implying the issue is present), the script raises an `AssertionError` and prints a stack trace.
6. If there are no issues detected, the script exits normally.