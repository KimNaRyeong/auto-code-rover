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

def reproduce_issue():
    try:
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        data = np.outer(y, y)
        myplot = plt.contour(x, y, data, levels=[100])
        print(myplot.levels)
        assert len(myplot.levels) == 1 and myplot.levels[0] == 0.0, "Expected contour levels to be [100]"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
