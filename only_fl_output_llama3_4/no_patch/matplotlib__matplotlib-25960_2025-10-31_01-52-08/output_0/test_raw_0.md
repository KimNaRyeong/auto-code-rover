Here is the reproducer script:

```python
import matplotlib.pyplot as plt
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

def reproduce_issue():
    figs = plt.figure().subfigures(2, 2, wspace=0, hspace=0)
    for fig in figs.flat:
        fig.subplots().plot([1, 2])
    f = StringIO()
    with redirect_stdout(f):
        plt.show()
    output = f.getvalue()
    if "Figure" not in output and "subfigures" not in output:
        raise AssertionError("Issue is present")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)