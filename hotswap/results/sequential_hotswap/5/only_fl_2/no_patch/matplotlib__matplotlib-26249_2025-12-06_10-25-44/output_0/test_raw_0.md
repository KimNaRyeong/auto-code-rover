 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    try:
        ax.scatter([1,np.nan,3], [2,np.nan,4], [3, np.nan,5], color=[[.5,.5,.5,.5]]*3, s=11.5)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    reproduce_issue()
```
This script will raise an `AssertionError` with the stack trace when executed with `python3 reproducer.py`. The line numbers of the statements in the stack trace may differ from the ones in the issue description, but the error message and the cause of the issue should be the same.