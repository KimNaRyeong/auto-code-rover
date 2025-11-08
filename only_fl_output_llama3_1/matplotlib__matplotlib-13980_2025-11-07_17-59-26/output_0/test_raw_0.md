Here is the reproducer script:

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
    try:
        np.random.seed(0)  # For reproducibility
        npoints = 10_000
        theta = 360 * np.random.random(npoints)
        r = np.random.random(npoints)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), dpi=120, facecolor='white', subplot_kw=dict(projection='polar'))
        ax1.plot(np.radians(theta), r, 'o', markersize=1)
        ax1.set_title('expected', pad=12)
        ax2.plot(np.radians(theta), r, 'o', markersize=1)
        ax2.set_title('unexpected', pad=12)
        ax1.set_ylim(bottom=0)
        # ax2.set_ylim(bottom=0)

        if not (ax2.get_ylim() == (0, 1.)):
            raise AssertionError("Non-sensical negative radial scale minimum autoset in polar plot")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the code that reproduces the issue and check if the y-limits of the second subplot are not (0, 1). If they are not, it will raise an AssertionError with a stack trace.