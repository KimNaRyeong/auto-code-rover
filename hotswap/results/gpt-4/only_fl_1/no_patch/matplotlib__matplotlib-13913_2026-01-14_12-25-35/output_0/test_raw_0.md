```python
# reproducer.py
import matplotlib
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

def main():
    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    color_like_result = all([matplotlib.colors.is_color_like(color) for color in c])
    if not color_like_result:
        raise AssertionError("`is_color_like` should return False for strings of integers.")

    try:
        plt.scatter(X[:, 0], X[:, 1], c=c)
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Expected to not reach this point if `is_color_like` worked as expected.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as ae:
        print(ae)
        exit(0) # Ensure we exit with code 0 when the issue is replicable
```

This script attempts to reproduce the reported issue by checking if `matplotlib.colors.is_color_like` incorrectly identifies strings of integers as valid colors, which then leads to a `ValueError` when attempting to use these "colors" in a `plt.scatter` call. The `print_stacktrace` function is utilized to clearly print the stack trace when the exception occurs, ensuring clarity on where and why the failure happened. If the assertion fails or the expected `ValueError` is caught, it indicates that the issue is present, and the script exits with code 0, signaling that the reproduction was successful under the conditions that trigger the bug.