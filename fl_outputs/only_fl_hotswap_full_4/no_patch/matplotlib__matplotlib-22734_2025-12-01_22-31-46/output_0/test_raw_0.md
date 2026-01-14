 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    np.random.seed(0)
    fig, ax = plt.subplots()
    tripcolor = ax.tripcolor
    tripcolor(np.random.rand(100), np.random.rand(100), np.random.rand(100), clim=(0, 0.5))
    cbar = fig.colorbar(ax.get_children()[-1])
    ax.set_title("tripcolor with clim=(0, 0.5)")
    cbar.set_label("Value")
    plt.show()

    expected_clim = (0, 0.5)
    image = ax.get_images()[0]
    actual_clim = image.get_clim()
    assert actual_clim == expected_clim, f"Expected clim: {expected_clim}, actual clim: {actual_clim}"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present. The script will exit with code 0 if the issue is fixed.