```python
import numpy as np
import sklearn.metrics
import sys

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

def test_label_ranking_average_precision_score():
    # The label and scores arrays to be used in the example
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=np.bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    sample_weight = [1.0, 1.0, 0.0]

    # The expectation is that the reported average precision score
    # would be an average of the scores of the first two samples only,
    # as the last one has a weight of 0.
    # These are 0.5 ((1/2) for the first sample), and 0.75 ((1+1/2)/2 for the second sample).
    expected_result = 0.625

    try:
        # Calculating the Label Ranking Average Precision Score
        result = sklearn.metrics.label_ranking_average_precision_score(
            truth, scores, sample_weight=sample_weight)

        # Asserting the expectation
        assert np.isclose(result, expected_result), f"Expected result: {expected_result}, Got: {result}"
        print("Test passed, the issue is fixed.")
    except AssertionError as e:
        # If AssertionError is caught, it means the test failed.
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_label_ranking_average_precision_score()
```

This script will perform the test as described, utilizing the provided `print_stacktrace` function to output a detailed stack trace if the assertion fails, indicating the presence of the issue. Once the issue is resolved (i.e., when the calculated result matches the expected result), the script will print a confirmation message and exit with code 0.