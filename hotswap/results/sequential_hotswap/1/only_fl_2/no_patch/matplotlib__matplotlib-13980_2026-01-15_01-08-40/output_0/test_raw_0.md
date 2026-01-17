```python
# reproducer.py
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
    npoints = 10_000
    theta = 360 * np.random.random(npoints)
    r = np.random.random(npoints)

    fig, ax2 = plt.subplots(figsize=(4, 2), dpi=120, facecolor='white', subplot_kw=dict(projection='polar'))
    ax2.plot(np.radians(theta), r, 'o', markersize=1)
    ax2.set_title('unexpected', pad=12)
    # ax2.set_ylim(bottom=0) # The line that's commented out to demonstrate the issue
    
    ymin, ymax = ax2.get_ylim()

    try:
        assert ymin >= 0, "Negative radial scale minimum auto-set in polar plot."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code when issue is present

    print("No issues detected.")  # This message should print if the assertion passes
    plt.show()

if __name__ == "__main__":
    main()
```