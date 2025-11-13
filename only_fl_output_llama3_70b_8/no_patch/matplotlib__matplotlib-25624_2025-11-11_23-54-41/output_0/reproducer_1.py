import matplotlib.pyplot as plt
import matplotlib.rcsetup as rc

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

plt.rcParams['figure.autolayout'] = True
fig, axes = plt.subplots(ncols=2)
fig.tight_layout(w_pad=10)

# Get the bounding box of the axes in display coordinates
bbox = axes[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())

try:
    assert bbox.width > 400, "tight layout kwargs have no effect"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
