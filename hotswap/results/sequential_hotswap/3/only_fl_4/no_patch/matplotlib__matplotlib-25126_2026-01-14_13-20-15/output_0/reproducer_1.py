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

def verify_plot_persistence_after_yscale_change():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    fig, ax = plt.subplots()
    # Ensure use of Agg backend for consistent behavior across environments
    canvas = FigureCanvas(fig)
    
    samples = np.random.normal(size=1000)
    x = np.linspace(-5, 5, 1000)
    ax.hist(samples, bins=50, log=True, density=True)
    line, = ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi))

    # Save the plot with log scale
    canvas.draw()
    renderer_log = canvas.get_renderer()
    data_log = renderer_log.buffer_rgba()

    # Change yscale to linear and save the plot again
    ax.set_yscale('linear')

    canvas.draw()
    renderer_linear = canvas.get_renderer()
    data_linear = renderer_linear.buffer_rgba()

    # Compare the two images; if they are identical, the line disappeared after yscale change.
    if np.array_equal(data_log, data_linear):
        raise AssertionError("Plot appearance did not change after yscale change; possible disappearance of plot elements.")

    print("Plot appearance changes observed, suggesting the plot persists correctly across yscale changes.")

try:
    verify_plot_persistence_after_yscale_change()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with a non-zero code to indicate an error / presence of issue
else:
    exit(0)  # Exit with zero to indicate the absence of the issue
