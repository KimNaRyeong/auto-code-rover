 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import seaborn as sns
import numpy as np
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def custom_min(x):
    return float(np.asarray(x).min())

def main():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    main()
```
This script imports the necessary modules, defines the `print_stacktrace` function, defines the `custom_min` function, and then defines the `main` function that reproduces the issue. If the issue is present, the script will print a stack trace and raise an `AssertionError`. If the issue is fixed, the script will exit with code 0.