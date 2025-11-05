import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from contextlib import redirect_stdout

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

def reproduce_bug():
    try:
        test = np.full((2, 1), -1)
        plt.imshow(test)
        plt.show(block=False)
        input("Press Enter to continue...")
    except Exception as e:
        f = StringIO()
        with redirect_stdout(f):
            print_stacktrace(e)
        print(f.getvalue(), flush=True)
        raise AssertionError("Bug reproduced")

if __name__ == "__main__":
    reproduce_bug()
