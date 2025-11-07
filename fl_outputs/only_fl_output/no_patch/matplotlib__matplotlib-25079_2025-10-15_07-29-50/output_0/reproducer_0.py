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
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    import numpy as np

    # Supress potential display issues when running without a GUI
    plt.switch_backend('agg')

    # Try to reproduce the issue.
    try:
        # create some random data to fill a 2d plot
        rng = np.random.default_rng(0)
        img = rng.uniform(1, 5, (25, 25))

        # plot it
        fig, ax = plt.subplots()
        plot = ax.pcolormesh(img)
        cbar = fig.colorbar(plot, ax=ax)

        vmin, vmax = 1, 5
        plot.set_norm(LogNorm(vmin, vmax))
        plot.autoscale()
        fig.canvas.draw_idle()  # Trigger a redraw to force potential error

        # Ensure norm is set as expected
        assert plot.norm.vmin == vmin and plot.norm.vmax == vmax

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    main()
    print("The issue seems to be resolved, exiting with code 0.")
    exit(0)
