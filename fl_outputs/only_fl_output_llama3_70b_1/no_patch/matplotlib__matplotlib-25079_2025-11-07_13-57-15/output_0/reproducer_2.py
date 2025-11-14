import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
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

    plot.norm = LogNorm(vmin, vmax)  # This line should raise an error
    plot.autoscale()
    plt.pause(0.5)
except ValueError as e:
    if "Invalid vmin or vmax" in str(e):
        print_stacktrace(e)
        raise AssertionError("Issue is present")
else:
    raise AssertionError("Issue is not present")
