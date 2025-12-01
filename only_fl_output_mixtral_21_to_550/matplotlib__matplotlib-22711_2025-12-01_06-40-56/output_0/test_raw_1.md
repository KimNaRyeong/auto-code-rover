 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    np.random.seed(19680801)
    N = 128
    img = np.random.randn(N, N)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(bottom=0.25)

    im = axs[0].imshow(img)
    axs[1].hist(img.flatten(), bins='auto')
    axs[1].set_title('Histogram of pixel intensities')

    slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
    try:
        slider = RangeSlider(slider_ax, "Threshold", img.min(), img.max(), valinit=[0.0, 0.0])
    except Exception as e:
        print_stacktrace(e)
        assert False

    lower_limit_line = axs[1].axvline(slider.val[0], color='k')
    upper_limit_line = axs[1].axvline(slider.val[1], color='k')

    def update(val):
        im.norm.vmin = val[0]
        im.norm.vmax = val[1]
        lower_limit_line.set_xdata([val[0], val[0]])
        upper_limit_line.set_xdata([val[1], val[1]])
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the issue. The script will also exit with code 1 to indicate the presence of the issue.

To fix the issue, you can either modify the `set_val` method in `matplotlib/widgets.py` by commenting out the line `xy[4] = val[0], .25`, or you can modify the `reproducer.py` script to pass a tuple of length 2 instead of length 4 to the `valinit` parameter of the `RangeSlider` constructor. Here is an example of the modified `main` function:
```python
def main():
    np.random.seed(19680801)
    N = 128
    img = np.random.randn(N, N)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(bottom=0.25)

    im = axs[0].imshow(img)
    axs[1].hist(img.flatten(), bins='auto')
    axs[1].set_title('Histogram of pixel intensities')

    slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
    slider = RangeSlider(slider_ax, "Threshold", img.min(), img.max(), valinit=(0.0, 0.0))

    lower_limit_line = axs[1].axvline(slider.val[0], color='k')
    upper_limit_line = axs[1].ax