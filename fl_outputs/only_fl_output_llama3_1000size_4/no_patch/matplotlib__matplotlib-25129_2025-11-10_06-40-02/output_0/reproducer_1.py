import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

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
    fig, ax = plt.subplots()
    ax.plot([1,2,3], [1,2,3])
    cursor = Cursor(ax, useblit=False, linewidth=1)
    plt.show()
except AssertionError as e:
    print_stacktrace(e)
    raise
finally:
    if not isinstance(e, AssertionError):
        print("Issue is fixed")
        exit(0)
