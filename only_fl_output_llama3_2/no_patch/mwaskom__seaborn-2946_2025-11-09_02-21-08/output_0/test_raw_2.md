Here is the reproducer script:

```python
import seaborn as sns
import numpy as np
from io import StringIO
from functools import wraps

def custom_min(x):
    return float(np.asarray(x).min())

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
        tips = sns.load_dataset("tips")
        def custom_min(x):
            return float(np.asarray(x).min())
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Regression: pointplot and barplot raise when using a custom estimator"

if __name__ == "__main__":
    reproducer()
```

This script will reproduce the issue by loading the `tips` dataset from seaborn, defining a custom minimum function, and then attempting to create a point plot with the `pointplot` function. If the error occurs, it will print the stack trace and fail the assertion, indicating that the regression is present.

Please note that this reproducer requires matplotlib installed in your environment.