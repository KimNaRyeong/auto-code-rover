```python
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

def test_hist_gradient_boosting_classifier_with_string_target_and_early_stopping():
    import numpy as np
    from sklearn.experimental import enable_hist_gradient_boosting  # noqa
    from sklearn.ensemble import HistGradientBoostingClassifier

    X = np.random.randn(100, 10)
    y = np.array(['x'] * 50 + ['y'] * 50, dtype=object)
    gbrt = HistGradientBoostingClassifier(n_iter_no_change=10)
    try:
        gbrt.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("HistGradientBoostingClassifier should not raise an exception when fitting with string labels and early stopping turned on.")

if __name__ == "__main__":
    test_hist_gradient_boosting_classifier_with_string_target_and_early_stopping()
```
This Python script, `reproducer.py`, is designed to test whether the `HistGradientBoostingClassifier` from Scikit-learn can handle string labels when early stopping is enabled. This is to reproduce the reported issue where an error is thrown in this scenario.

The script follows the provided instructions for reproducing the problem. It tries to train a `HistGradientBoostingClassifier` with a dataset that has string labels (`'x'` and `'y'`). Early stopping is enabled via the `n_iter_no_change` parameter.

If the classifier is unable to handle string labels with early stopping and raises an exception, the script captures this exception, prints a detailed stack trace (including line numbers and code context), and raises an `AssertionError` to indicate the failure of the test. 

The `print_stacktrace` function is used to ensure that the stack trace is printed in a readable format, emphasizing the recent calls that lead to the exception, making it easier to identify the potential bug in the implementation.

Should the issue in question be fixed, this script will execute without raising an `AssertionError`, and it will exit with code 0, indicating the problem is resolved.