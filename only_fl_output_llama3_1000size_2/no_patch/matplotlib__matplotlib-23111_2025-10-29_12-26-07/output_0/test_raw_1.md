Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from contextlib import redirect_stdout
import sys

def print_stacktrace(e: Exception):
    import traceback
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
        import matplotlib.pyplot as plt
        import numpy as np

        test = np.full((2, 1), -1)
        f = StringIO()
        with redirect_stdout(f):
            plt.imshow(test)
            plt.show()
        output = f.getvalue().strip()
        if "ValueError: math domain error" in output:
            raise AssertionError("Bug reproduced")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_bug()
```

This script will attempt to reproduce the bug by calling `plt.imshow` with an array of all negative values. It will capture the output and check if it contains the error message "ValueError: math domain error". If the bug is present, it will raise an `AssertionError`.