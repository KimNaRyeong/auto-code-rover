Here is the reproducer script:

```python
#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import sys
from functools import wraps

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

def reproducer():
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        plt.style.use('_mpl-gallery')

        # make data
        x = np.linspace(0, 10, 100)
        y = 4 + 2 * np.sin(2 * x)

        # plot
        fig, ax = plt.subplots()

        ax.plot(x, y, linewidth=2.0)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
               ylim=(0, 8), yticks=np.arange(1, 8))

        plt.savefig("sin.jpg", metadata={})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproducer()
```

This script will reproduce the issue and print a stack trace when it fails.