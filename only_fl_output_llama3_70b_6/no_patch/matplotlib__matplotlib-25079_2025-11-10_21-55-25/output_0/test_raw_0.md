Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

def main():
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

    try:
        plot.norm = LogNorm(vmin, vmax)
        plot.autoscale()
        plt.pause(0.5)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Setting norm with existing colorbar fails"

if __name__ == "__main__":
    main()

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
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.