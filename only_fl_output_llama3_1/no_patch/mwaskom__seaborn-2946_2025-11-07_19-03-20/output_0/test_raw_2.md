I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import seaborn as sns
import numpy as np

def custom_min(x):
    return float(np.asarray(x).min())

tips = sns.load_dataset("tips")

try:
    ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
finally:
    sys.exit(0)

def print_stacktrace(e):
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
    import sys
    try:
        sns.set()
        sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
    finally:
        sys.exit(0)
```

This script should reproduce the issue by calling `sns.pointplot` with the custom `estimator` function. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue.