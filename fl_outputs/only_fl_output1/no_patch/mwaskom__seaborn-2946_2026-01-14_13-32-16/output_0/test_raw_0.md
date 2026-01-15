```python
# reproducer.py

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

def test_seaborn_custom_estimator():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
        print("No issue found. The custom estimator works as expected.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue detected with custom estimator in seaborn.")

if __name__ == "__main__":
    test_seaborn_custom_estimator()
```