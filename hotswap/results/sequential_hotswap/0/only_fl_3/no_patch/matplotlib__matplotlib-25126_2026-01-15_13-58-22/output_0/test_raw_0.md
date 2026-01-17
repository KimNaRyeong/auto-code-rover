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

def assert_plots_are_not_empty(fig, msg):
    import matplotlib.pyplot as plt
    has_content = False
    for ax in fig.axes:
        for child in ax.get_children():
            if isinstance(child, plt.Line2D):
                xdata, ydata = child.get_data()
                if len(xdata) > 0 and len(ydata) > 0:
                    has_content = True
                    break
    if not has_content:
        raise AssertionError(msg)

try:
    import numpy as np
    import matplotlib.pyplot as plt
    
    samples = np.random.normal(size=1000)
    x = np.linspace(-5, 5, 1000)
    fig, ax = plt.subplots()
    ax.hist(samples, log=True, density=True)
    ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi))
    fig.savefig('log_before_assertion.pdf')
    assert_plots_are_not_empty(fig, "Plot disappeared after creating log-scaled histogram.")
    
    ax.set_yscale('linear')
    fig.savefig('lin_before_assertion.pdf')
    assert_plots_are_not_empty(fig, "Plot disappeared after switching to linear scale.")

except AssertionError as e:
    print_stacktrace(e)
    exit(1)
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script starts by importing necessary modules to reproduce the issue. It defines a utility function `print_stacktrace` for printing exceptions, and another utility `assert_plots_are_not_empty` to check whether plots are not empty (i.e., they contain data lines).

It executes steps to reproduce the stated issue:

1. Generate a sample and a plot with a logarithmic histogram.
2. Save the figure.
3. Uses `assert_plots_are_not_empty` to confirm that the plot has lines before changing y-scale.
4. Change the y-scale to linear.
5. Saves the figure again.
6. Uses `assert_plots_are_not_empty` again to confirm that the plot still has lines after changing y-scale.

The script will exit with code `1` and print a stack trace if the plot disappears after changing the y-scale, indicating the issue is present. If the plot does not disappear, it exits with code `0`, indicating the issue is fixed or not present.