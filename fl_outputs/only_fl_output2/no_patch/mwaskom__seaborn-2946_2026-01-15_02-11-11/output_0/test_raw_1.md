Given the specific requirements and to ensure that the script correctly reproduces the issue while adhering to your guidelines for handling success and failure cases, the following Python script `reproducer.py` is crafted. This version carefully integrates the provided function for printing stack traces of exceptions, raising an `AssertionError` if the issue persists and exiting gracefully with code 0 if the issue is no longer present.

```python
# reproducer.py

import sys

try:
    import seaborn as sns
    import numpy as np
except ImportError as e:
    print("Required libraries (seaborn, numpy) are not installed.")
    raise e

def print_stacktrace(e: Exception):
    import traceback
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

def test_seaborn_custom_estimator():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        return False
    return True

def main():
    result = test_seaborn_custom_estimator()
    if not result:
        raise AssertionError("Failed: Issue with custom estimator in pointplot/barplot detected.")
    else:
        print("Succeeded: No errors found with the custom estimator.")

if __name__ == "__main__":
    main()
    sys.exit(0)
```

This script aims to specifically target the behavior of seaborn `pointplot` and `barplot` functions when provided with a custom `estimator`. It follows the instructions to trigger an `AssertionError` when the issue with the custom estimator is reproduced, and it exits gracefully with code 0 if the issue is resolved or not present, as per the provided issue reproduction criteria. Remember to have seaborn and numpy installed in your environment before running this script.