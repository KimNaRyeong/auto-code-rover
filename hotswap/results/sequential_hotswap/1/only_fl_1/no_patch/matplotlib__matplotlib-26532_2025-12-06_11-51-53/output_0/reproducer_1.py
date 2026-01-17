import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [0, 1, 1, 0, 0]
    y = [0, 0, 1, 1, 0]
    z = [0, 0, 0, 1, 1]

    try:
        poly = Poly3DCollection([[[x[i], y[i], z[i]] for i in range(5)]])
        ax.add_collection3d(poly, shade=True)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Test failed. The above stack trace should indicate the TypeError."

if __name__ == "__main__":
    main()
    assert True, "Test passed."
