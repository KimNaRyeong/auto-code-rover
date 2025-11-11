import matplotlib.pyplot as plt
from io import StringIO
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

def reproduce_issue():
    try:
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25)
        ax.plot(10, 10, color='g', alpha=1.0, marker="$\star$", markersize=25)
        ax.plot(10, 10, color='r', alpha=1.0, marker=".")
        plt.show(block=True)  # This is the key line
        assert False, "Markers should be center-aligned"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
