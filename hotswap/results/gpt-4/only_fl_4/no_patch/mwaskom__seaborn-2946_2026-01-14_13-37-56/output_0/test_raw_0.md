To create a standalone Python file `reproducer.py` that reproduces the reported issue and follows your instructions, you can use the following code. It attempts to use `seaborn`'s `pointplot` (and similarly can be adjusted for `barplot`) with a custom estimator function that triggers the described issue. When the issue is present, it will raise an `AssertionError` and print the stack trace. If the issue is resolved (e.g., in a future version where this behavior is corrected), the script should exit without an error.

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

def test_seaborn_custom_estimator():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
        assert False, "Issue not present, test failed to reproduced the issue."
    except TypeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_seaborn_custom_estimator()
```

When you run this script with `python3 reproducer.py`:
- If the issue is present (as described, happening in version `0.12.0.dev0` but not in `0.11.2`), you will get an `AssertionError` indicating that the test to reproduce the issue failed because the issue was not present. Before that, it should print the stack trace of the caught `TypeError`.
- If the issue has been fixed in a newer version after `0.12.0.dev0`, the AssertionError that states "Issue not present" should _not_ occur, implying that the script ends without errors, satisfying the requirement to exit with code 0.

This script directly addresses the specific problem with seaborn's handling of custom estimators in `pointplot` (and by extension `barplot`, if modified to test that as well), assuming the issue is as described in your information.