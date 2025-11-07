Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np

def reproduce_issue():
    try:
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        data = np.random.uniform(0, 50, (100, 100))
        myplot = plt.contour(x, y, data, levels=[100])
        if myplot.levels != [100]:
            raise AssertionError("Expected contour levels to be [100], but got {}".format(myplot.levels))
    except AssertionError as e:
        print_stacktrace(e)

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

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3:

```bash
python3 reproducer.py
```

This script should raise an `AssertionError` when the issue is present, printing the stack trace of the error.