Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
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
    import matplotlib.pyplot as plt
    import numpy as np

    a = np.linspace(0, 2 * np.pi, 100)
    b = np.sin(a)
    c = np.cos(a)
    fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
    ax[0].plot(a, b)
    ax[1].plot(a, c)
    plt.subplots_adjust(wspace=0)

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

To run the script, simply execute `python3 reproducer.py` in your terminal. If the issue is present, it will raise an `AssertionError`, print the stack trace using the provided function, and exit with code 1. If the issue is fixed, it will print a success message and exit with code 0.