Given the feedback and the requirements, here's a tailored `reproducer.py` Python script intended to capture the essence of the issue regarding `pointplot` and `barplot` in seaborn with custom estimators. The script focuses on executing those specific plots with a custom estimator function to validate whether the issue persists. The function `print_stacktrace` is included as specified, to output detailed error messages if exceptions occur, aiding in diagnosing the problem accurately.

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
    return float(np.min(x))

def reproduce_issue_with_pointplot():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        return False
    return True

def reproduce_issue_with_barplot():
    tips = sns.load_dataset("tips")
    try:
        ax = sns.barplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        return False
    return True

def main():
    pointplot_test_passed = reproduce_issue_with_pointplot()
    barplot_test_passed = reproduce_issue_with_barplot()
    assert pointplot_test_passed and barplot_test_passed, "Failed: Regression detected in seaborn's pointplot or barplot with a custom estimator."

    print("Success: No issue detected with custom estimators.")

if __name__ == "__main__":
    main()
```

This script aims to be executed in the following manner:
1. It imports the required modules (`seaborn` and `numpy`).
2. Defines a `custom_min` function intended as a custom estimator for both `pointplot` and `barplot`.
3. Contains two specific functions to test `pointplot` and `barplot` separately.
4. Executes these tests within a `main` function, which evaluates the success of these plotting functions without issues.
5. Asserts the success of both tests, and prints a success message if no exceptions occur, or utilizes the `print_stacktrace` function to output detailed error information otherwise.

Please ensure seaborn is correctly installed in your environment (ideally `seaborn` version 0.11.2 or above, as mentioned in the issue description, and checking against the `0.12.0.dev0`) before running this script.