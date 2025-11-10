Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    c = np.full(10, np.nan)
    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
        raise AssertionError("Should warn when all values are bad")
    except UserWarning as e:
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
    main()
```
This script should raise an `AssertionError` when the issue is present, and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.