import matplotlib.pyplot as plt
import sys
from io import StringIO

def print_stacktrace(e: Exception):
    import traceback
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
        plt.rcParams.update({'ytick.labelcolor': 'red'})
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot([1.01e9, 1.02e9, 1.03e9])
        assert plt.gca().yaxis.get_offset_text().get_color() == (0.0, 0.0, 0.0), "Expected offset text color to be red"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
