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
    figs = plt.figure().subfigures(2, 2, wspace=0, hspace=0)
    for fig in figs.flat:
        fig.subplots().plot([1, 2])
    f = StringIO()
    with redirect_stdout(f):
        plt.show()
    output = f.getvalue()
    if "Figure size is" not in output:
        raise AssertionError("Expected 'Figure size is' in the output")

try:
    reproduce_bug()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Bug reproduced successfully. This means that the bug is still present.")
exit(0)
