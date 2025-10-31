Here is the reproducer script:

```python
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
        plt.ioff()
        fig, axes = plt.subplots(ncols=2)
        fig.tight_layout(w_pad=10)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a figure with two subplots using `plt.subplots()`, then attempts to use `fig.tight_layout()` with a non-zero w_pad. Since the issue is that tight layout kwargs have no effect if rc autolayout setting is set, this script should raise an AssertionError when run.