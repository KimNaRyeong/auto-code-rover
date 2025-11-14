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

try:
    test = np.full((2, 1), -1)
    fig, ax = plt.subplots()
    ax.imshow(test)
    plt.show(block=False)  # show the plot without blocking
    import time
    time.sleep(1)  # wait for a second to allow the plot to render
    assert plt.gca().axes.xaxis.get_label()._xform_cache['major'] is not None, "Math domain error occurred"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Math domain error occurred")
