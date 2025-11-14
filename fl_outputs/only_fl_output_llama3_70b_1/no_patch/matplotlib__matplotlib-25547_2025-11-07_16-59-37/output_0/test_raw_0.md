Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import matplotlib.pyplot as plt

def test_issue():
    c = np.full(10, np.nan)
    c[0] = 1.
    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert False, "Should not warn when some values are bad"

    try:
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert True, "Should warn when all values are bad"
    else:
        assert False, "Should warn when all values are bad"

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

test_issue()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.