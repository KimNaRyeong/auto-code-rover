Certainly! Below is a standalone Python file `reproducer.py` designed to reproduce the issue as you described:

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

def test_label_ranking_average_precision_score():
    import numpy as np
    import sklearn.metrics

    # Per sample APs are 0.5, 0.75, and 1.0 (default for zero labels).
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    try:
        expected_result = 0.625
        actual_result = sklearn.metrics.label_ranking_average_precision_score(truth, scores, sample_weight=[1.0, 1.0, 0.0])
        assert abs(actual_result - expected_result) < 1e-9, \
            f"Expected result: {expected_result}, but got: {actual_result}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == '__main__':
    try:
        test_label_ranking_average_precision_score()
    except AssertionError:
        import sys
        sys.exit(1)
    else:
        sys.exit(0)
```

This script performs the following:

1. Defines a function `test_label_ranking_average_precision_score()` which:
    - Prepares sample inputs for the function `label_ranking_average_precision_score` including labels (`truth`), scores, and a sample weight where one of the samples is intended to have no weight (analogous to expecting that it shouldn't affect the final score).
    - Calls this function with the prepared inputs.
    - Checks whether the actual output matches the expected average precision score, which according to the provided description should be the average of the first two samples since the third has a weight of 0. The assertion fails if this is not the case, indicating a potential problem.
2. Uses `try...except` blocks to catch any `AssertionError` thrown due to a mismatch between expected and actual results and prints a more detailed stack trace using `print_stacktrace()` for debugging purposes.
3. Uses a main block to run the test, exiting with code 1 (indicative of error) if an assertion error is caught, or exiting with code 0 (indicative of success) if no error occurs.

If the issue is present, execution of this script should result in an `AssertionError` showing that the function failed to properly account for the sample weights when some labels have zero true values, hence not matching the expected result.