Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn.metrics import label_ranking_average_precision_score

def main():
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=np.bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    sample_weight = [1.0, 1.0, 0.0]

    try:
        ap = label_ranking_average_precision_score(truth, scores, sample_weight=sample_weight)
        assert ap == 0.625
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script reproduces the issue by calling `label_ranking_average_precision_score` with a sample weight vector that contains zeros, and then asserts that the returned average precision is equal to 0.625. If an exception is raised during the execution of this script, it prints the stack trace and raises the exception.

Please note that you need to have scikit-learn installed in your Python environment for this script to work correctly.