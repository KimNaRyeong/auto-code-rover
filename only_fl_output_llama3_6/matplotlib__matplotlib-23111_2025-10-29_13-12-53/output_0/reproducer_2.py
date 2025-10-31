import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from contextlib import redirect_stdout
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

def reproduce_bug():
    try:
        test = np.full((2, 1), -1)
        plt.imshow(test)
        plt.show()
        if True:  # This will never be true
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_bug()
