```python
# reproducer.py
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

def test_issue():
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    import numpy as np

    try:
        # create some random data to fill a 2d plot
        rng = np.random.default_rng(0)
        img = rng.uniform(1, 5, (25, 25))

        # plot it
        fig, ax = plt.subplots(layout="constrained")
        plot = ax.pcolormesh(img)
        cbar = fig.colorbar(plot, ax=ax)

        vmin = 1
        vmax = 5

        plt.ion()
        fig.show()
        plt.pause(0.5)

        plot.norm = LogNorm(vmin, vmax)
        plot.autoscale()
        plt.pause(0.5)

        # The call to plt.pause might not raise an exception directly, 
        # so check if the issue is fixed by plotting again and looking for exceptions.
        try:
            fig.canvas.draw_idle()
        except Exception as e:
            raise AssertionError("Issue is present") from e

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_issue()
    print("Issue not present.")
```

This script aims to reproduce the issue described, where setting the norm to `LogNorm` after the colorbar has been created leads to an `Invalid vmin` error in Matplotlib version 3.6.3. It uses an `AssertionError` to indicate when the issue is present based on whether an exception is raised during runtime. It uses the function `print_stacktrace` to provide a clear trace of where the exception occurred. Also, it exits with code 0 (`exit(1)` is used to exit non-zero when an error occurs for clarity, but this script does not explicitly exit with 0 when successful because the default exit code is 0 if the script completes without encountering uncaught exceptions).