import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import traceback
import sys

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
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
    ax1.scatter([1], [1], [1])
    ax2.scatter([1], [1], [1], c='r')
    assert not ax1.get_visible(), "set_visible(False) should make the subplot invisible"
    plt.show()
except AssertionError as e:
    print_stacktrace(e)
    raise
finally:
    if not hasattr(globals(), 'plt'):
        print("Issue is present")
        exit(1)
    else:
        print("Issue is fixed")
        exit(0)
