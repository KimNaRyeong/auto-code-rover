import matplotlib.pyplot as plt
import numpy as np

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

# Create a sample polygon
poly = plt.Polygon(np.array([[0, 0], [1, 0], [1, 1], [0, 1]]))

# Create some sample data
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)
data = X**2 + Y**2

try:
    # Try to reproduce the issue
    plt.contourf(X, Y, data, clip_path=poly)
    assert False, "clip_path kwarg should be ignored"
except TypeError:
    print("Issue reproduced successfully")
    print_stacktrace(e)
else:
    print("Issue not present")

plt.show()
