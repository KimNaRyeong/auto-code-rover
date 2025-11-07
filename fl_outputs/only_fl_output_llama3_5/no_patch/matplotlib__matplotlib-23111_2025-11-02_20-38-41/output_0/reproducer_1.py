import matplotlib.pyplot as plt
import numpy as np

def reproduce_issue():
    try:
        test = np.full((2, 1), -1)
        plt.imshow(test)
        plt.show()
        hover_info = plt.ginput(-1)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

    if len(hover_info) == 0:
        raise AssertionError("Issue not reproduced")

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

if __name__ == "__main__":
    reproduce_issue()
