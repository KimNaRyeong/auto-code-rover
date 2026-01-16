```python
# reproducer.py
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

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

def change_tick_color():
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.scatter((0, 0, 1), (0, 1, 0), (1, 0, 0))
    ax.w_xaxis.line.set_color('red')
    ax.w_yaxis.line.set_color('red')
    ax.w_zaxis.line.set_color('red')
    ax.xaxis.label.set_color('red')
    ax.yaxis.label.set_color('red')
    ax.zaxis.label.set_color('red')
    ax.tick_params(axis='x', colors='red')
    ax.tick_params(axis='y', colors='red')
    ax.tick_params(axis='z', colors='red')

    # Checking if tick marks color changed to red
    # Unfortunately, we can't check the color of tick markers directly,
    # so we will simulate a failure to demonstrate AssertionError
    # In practice, this part of the code is supposed to check whether the issue is fixed or not.
    try:
        assert ax.w_xaxis._axinfo['tick']['color'] == 'red', "Tick mark color for x-axis not set to red."
        assert ax.w_yaxis._axinfo['tick']['color'] == 'red', "Tick mark color for y-axis not set to red."
        assert ax.w_zaxis._axinfo['tick']['color'] == 'red', "Tick mark color for z-axis not set to red."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code when the issue is present

    print("Tick mark color successfully changed.")

if __name__ == "__main__":
    change_tick_color()
```