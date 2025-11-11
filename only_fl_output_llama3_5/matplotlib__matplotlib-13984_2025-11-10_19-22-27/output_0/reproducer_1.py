import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    ax = Axes3D(fig, auto_add_to_figure=False)  # add this line to suppress the warning

    ax.scatter((0, 0, 1), (0, 1, 0), (1, 0, 0))
    ax.w_xaxis.line.set_color('red')
    ax.w_yaxis.line.set_color('red')
    ax.w_zaxis.line.set_color('red')
    ax.xaxis.label.set_color('red')
    ax.yaxis.label.set_color('red')
    ax.zaxis.label.set_color('red')

    # This line should raise an AssertionError if the issue is present
    assert ax.tick_params(axis='x', colors='red') == ax  # only affects tick labels

    fig.show()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed, reproducer script did not raise an AssertionError.")
exit(0)
