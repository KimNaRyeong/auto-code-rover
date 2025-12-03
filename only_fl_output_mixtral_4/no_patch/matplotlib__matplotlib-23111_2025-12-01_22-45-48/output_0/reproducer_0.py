import matplotlib.pyplot as plt
import numpy as np
import sys

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

test = np.full((2, 1), -1)
plt.imshow(test)
plt.show()

# The following line should raise an AssertionError
assert False, "Math domain errors should have been raised, but they weren't."
