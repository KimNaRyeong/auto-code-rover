```python
import numpy as np
import sklearn.metrics

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
    # Per sample APs are 0.5, 0.75, and 1.0 (default for zero labels).
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=np.bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    expected_result = 0.625
    try:
        result = sklearn.metrics.label_ranking_average_precision_score(
            truth, scores, sample_weight=[1.0, 1.0, 0.0])
        assert np.isclose(result, expected_result), (
            f"Expected result {expected_result}, but got {result}"
        )
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        test_label_ranking_average_precision_score()
    except AssertionError:
        # Exit with an error code when the issue is present.
        exit(1)
    # Exit cleanly if everything is correct.
    exit(0)
```