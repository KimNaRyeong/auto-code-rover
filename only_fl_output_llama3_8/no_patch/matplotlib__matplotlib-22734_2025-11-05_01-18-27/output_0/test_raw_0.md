Here is the reproducer script:

```python
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

def reproduce_issue():
    try:
        from pylab import *
        tripcolor(np.random.rand(100), np.random.rand(100), np.random.rand(100), clim=(0, 0.5))
        colorbar()
        show()
    except Exception as e:
        f = StringIO()
        with redirect_stdout(f):
            print_stacktrace(e)
        print(f.read(), file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by calling `tripcolor` and checking if it ignores the `clim`. If an exception is raised, it will print the stack trace and exit with code 1.