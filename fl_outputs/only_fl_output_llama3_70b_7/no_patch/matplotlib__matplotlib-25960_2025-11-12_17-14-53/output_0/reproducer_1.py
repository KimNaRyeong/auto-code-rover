import matplotlib.pyplot as plt
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

figs = plt.figure().subfigures(2, 2, wspace=0.5, hspace=0.5)
for fig in figs.flat:
    fig.subplots().plot([1, 2])
plt.show()

# Check if the figure is rendered correctly
import matplotlib as mpl
assert mpl.rcParams['figure.subplot.wspace'] == 0.5, "wspace not applied"
assert mpl.rcParams['figure.subplot.hspace'] == 0.5, "hspace not applied"

try:
    assert figs[0].get_subplot_params()['wspace'] == 0.5, "wspace not applied to subfigures"
    assert figs[0].get_subplot_params()['hspace'] == 0.5, "hspace not applied to subfigures"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
