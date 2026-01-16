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
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        import os

        # Reproduce the issue
        samples = np.random.normal(size=1000)
        x = np.linspace(-5, 5, 1000)
        fig, ax = plt.subplots()

        ax.hist(samples, bins=30, log=True, density=True)
        line = ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi))

        # Save the figure with log scale
        fig.savefig('log.pdf')

        # Change to a linear scale
        ax.set_yscale('linear')

        # Attempt to force redrawing to verify if elements persist correctly
        fig.canvas.draw()

        # Save the figure with linear scale
        fig.savefig('lin.pdf')

        # Check if the line is still visible after scale change
        if not line[0].get_visible():
            raise AssertionError("Line disappears after changing y_scale from 'log' to 'linear'.")

    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```