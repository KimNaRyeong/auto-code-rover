Certainly! In response to the requirement for a standalone Python script that checks for the specific issue mentioned and conforms precisely to the instructions given, here's how you can structure `reproducer.py`. This script is designed to assess the problem with sample weighting in `label_ranking_average_precision_score` when dealing with samples that have zero true labels:

```python
import numpy as np
from sklearn.metrics import label_ranking_average_precision_score
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

def main():
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    sample_weight = np.array([1.0, 1.0, 0.0])

    try:
        calculated_score = label_ranking_average_precision_score(truth, scores, sample_weight=sample_weight)
        
        # Calculate the expected score manually factoring the sample weights
        expected_score = (0.5 * 1.0 + 0.75 * 1.0) / (1.0 + 1.0)  # Adjusting for sample_weights explicitly
        
        # Asserting the calculated and expected scores are equal
        assert np.isclose(calculated_score, expected_score), f"Expected score was {expected_score}, but the calculated score was {calculated_score}."
        print("No issue detected. Exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print("Issue detected.")
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

When executed, `reproducer.py` will raise an `AssertionError` if the issue is present, detailing the expected versus actual scores calculated by `label_ranking_average_precision_score`, while also printing a stack trace for clarity on the error's origin. Conversely, if the issue has been fixed, it will print a confirmation message and exit with code 0.
