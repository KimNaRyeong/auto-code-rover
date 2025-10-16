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
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RangeSlider

    # generate a fake image
    np.random.seed(19680801)
    N = 128
    img = np.random.randn(N, N)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(bottom=0.25)

    im = axs[0].imshow(img)
    axs[1].hist(img.flatten(), bins='auto')
    axs[1].set_title('Histogram of pixel intensities')

    # Create the RangeSlider
    slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
    slider = RangeSlider(slider_ax, "Threshold", img.min(), img.max(), valinit=[0.0, 0.0])

    # Create the Vertical lines on the histogram
    lower_limit_line = axs[1].axvline(slider.val[0], color='k')
    upper_limit_line = axs[1].axvline(slider.val[1], color='k')

    def update(val):
        im.norm.vmin = val[0]
        im.norm.vmax = val[1]

        lower_limit_line.set_xdata([val[0], val[0]])
        upper_limit_line.set_xdata([val[1], val[1]])

        fig.canvas.draw_idle()

    slider.on_changed(update)

    assert False, "The issue should raise an IndexError before this point."

except Exception as e:
    print_stacktrace(e)
    # To simulate a fixed bug, we'd want an assertion error if the specific expected exception is not thrown
    assert isinstance(e, IndexError), "Expected an IndexError due to a bug"
    sys.exit(0)
