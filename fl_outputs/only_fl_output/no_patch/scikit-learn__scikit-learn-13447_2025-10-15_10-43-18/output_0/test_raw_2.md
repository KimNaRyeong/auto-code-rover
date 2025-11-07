Certainly! Based on your requirements, here's a standalone Python file named `reproducer.py` which is designed to reproduce the issue involving the `label_ranking_average_precision_score` function from scikit-learn. This script checks if sample weighting is appropriately applied to items with zero true labels, and it raises an `AssertionError` if the observed behavior doesn't match the expected behavior indicative of the issue being fixed.

```python
import numpy as np
from sklearn.metrics import label_ranking_average_precision_score

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

def test_issue():
    # Example setup from the issue description
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    sample_weight = [1.0, 1.0, 0.0]
    try:
        # Calculating label ranking average precision score
        result = label_ranking_average_precision_score(truth, scores, sample_weight=sample_weight)
        
        # Expected result calculation considering the sample_weight properly
        expected_result = (0.5 + 0.75) / 2  # Only the first two samples should count

        assert np.isclose(result, expected_result), (
            f"Expected result {expected_result}, got {result}"
        )
        print("Issue resolved; test passed.")
        
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Reraises the AssertionError to indicate failure

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError:
        # Issue exists
        exit(1)
    else:
        # Issue resolved
        exit(0)
```

To use this script:

1. Save the script to a file named `reproducer.py` in the root directory of your project.
2. Execute the script using `python3 reproducer.py`.

The script checks if the sample weight is incorrectly applied (or not applied) to samples with all true or all false labels by comparing the calculated average precision score with an expected result. It uses an `AssertionError` to signal whether the issue is present or fixed, based on whether the actual result matches the expected one. If the issue is present, it will print a stack trace to help identify where the problem occurred.