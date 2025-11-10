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

x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
data = X**2 + Y**2

myplot = plt.contour(X, Y, data, levels=[100])
print(myplot.levels)

assert myplot.levels == [100], "Contour level autoscaling is not overridden"
    raise AssertionError("Contour level autoscaling is not overridden")

plt.show()
