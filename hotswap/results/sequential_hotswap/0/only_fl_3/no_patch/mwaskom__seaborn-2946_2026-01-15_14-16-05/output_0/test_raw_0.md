Below is the `reproducer.py` script designed to reproduce the issue as described. When you run this script with the affected version of seaborn (`0.12.0.dev0`), it should raise an `AssertionError` if the issue is present, print the stack trace of the issue, and exit successfully (return code 0) when the issue is fixed or not present.

```python
import seaborn as sns
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

def custom_min(x):
    return float(np.asarray(x).min())

def try_pointplot():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
        print("No issue with pointplot and custom estimator.")
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

def try_barplot():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.barplot(x="day", y="tip", data=tips, estimator=custom_min)
        print("No issue with barplot and custom estimator.")
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

def main():
    pointplot_success = try_pointplot()
    barplot_success = try_barplot()
    assert pointplot_success and barplot_success, "Regression detected in seaborn's pointplot or barplot with a custom estimator."

if __name__ == "__main__":
    main()
```

Make sure you have seaborn installed in your working environment before running this script. The script runs two tests: one with `pointplot` and another with `barplot`. Both use a custom function `custom_min` as the estimator. If either test raises an exception due to the issue you described, it will print a detailed stack trace. Otherwise, it will confirm that there's no issue with using custom estimators in `pointplot` or `barplot`.