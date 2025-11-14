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

def reproduce_bug():
    try:
        figs = plt.figure(subplots=True, figsize=(6, 4), wspace=0.5, hspace=1.0).subfigures(2, 2)
        for ax in figs.flat:
            ax.plot([1, 2])
        plt.show()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_bug()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace. If you run this script, it should reproduce the bug and print the expected output.