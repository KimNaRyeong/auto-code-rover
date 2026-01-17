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

def test_hist_gradient_boosting_classifier_early_stopping_with_string_target():
    import numpy as np
    from sklearn.experimental import enable_hist_gradient_boosting  # noqa: F401
    from sklearn.ensemble import HistGradientBoostingClassifier

    X = np.random.randn(100, 10)
    y = np.array(['x'] * 50 + ['y'] * 50, dtype=object)
    gbrt = HistGradientBoostingClassifier(n_iter_no_change=10, early_stopping=True)

    try:
        gbrt.fit(X, y)
        # If the code proceeds past this point, no error was encountered.
        # We raise an AssertionError to indicate that the expected issue did not occur.
        raise AssertionError("HistGradientBoostingClassifier did not raise an error with string target and early stopping.")
    except TypeError as e:
        print_stacktrace(e)
    except Exception as e:
        raise AssertionError("Unexpected exception type raised.") from e

if __name__ == "__main__":
    test_hist_gradient_boosting_classifier_early_stopping_with_string_target()
```
This script aims to reproduce the issue where `HistGradientBoostingClassifier` does not work with string targets when early stopping is turned on. It uses `print_stacktrace` to clearly show where the exception occurs if the expected `TypeError` is raised due to the issue outlined. If the issue is resolved (meaning no `TypeError` is raised), it throws an `AssertionError` with a message indicating the error did not occur as expected. This helps in validating whether the fix for the issue has been successfully applied or not by checking for exit code 0, which signifies no `AssertionError` was raised, thereby indicating the issue has been fixed.