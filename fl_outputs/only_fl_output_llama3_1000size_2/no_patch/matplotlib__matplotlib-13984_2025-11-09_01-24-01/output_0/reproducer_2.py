import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import traceback

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
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt

    fig = plt.figure()
    ax = Axes3D(fig)

    ax.scatter((0, 0, 1), (0, 1, 0), (1, 0, 0))
    ax.w_xaxis.line.set_color('red')
    ax.w_yaxis.line.set_color('red')
    ax.w_zaxis.line.set_color('red')
    ax.xaxis.label.set_color('red')
    ax.yaxis.label.set_color('red')
    ax.zaxis.label.set_color('red')

    ax.tick_params(axis='x', colors='red')  # only affects tick labels
    ax.tick_params(axis='y', colors='red')  # not tick marks
    ax.tick_params(axis='z', colors='red')  # not tick marks

    assert False, "Expected the tick mark color to be changed"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
