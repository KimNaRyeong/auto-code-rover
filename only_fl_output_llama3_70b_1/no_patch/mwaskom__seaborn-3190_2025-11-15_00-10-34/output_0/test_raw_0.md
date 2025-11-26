Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import seaborn as sns
import matplotlib.pyplot as plt

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
    sns.set()
    so = sns.load_dataset("tips")
    plt.figure(figsize=(8, 6))
    sns.Plot(["a", "b"], [1, 2], color=[True, False]).add(sns.Bar())
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Color mapping fails with boolean data")

print("No issue found. Exiting with code 0.")
```
This script will try to reproduce the issue by creating a plot with boolean color data using Seaborn. If the issue is present, it will catch the exception, print the stack trace, and raise an `AssertionError`. If the issue is fixed, it will simply print "No issue found. Exiting with code 0."