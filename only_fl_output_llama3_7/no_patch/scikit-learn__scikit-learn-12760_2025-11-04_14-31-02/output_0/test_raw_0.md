Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
from sklearn.metrics.cluster import davies_bouldin_score
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(0)
n_samples = 100
n_features = 2
X = np.random.rand(n_samples, n_features)

# Create clusters
labels = np.zeros(n_samples, dtype=int)
for i in range(n_samples):
    if i < 30:
        labels[i] = 0
    elif i < 60:
        labels[i] = 1
    else:
        labels[i] = 2

try:
    # Calculate Davies-Bouldin score
    db_score = davies_bouldin_score(X, labels)
    print(f"Davies-Bouldin score: {db_score}")
except RuntimeWarning as e:
    print_stacktrace(e)
    assert False, "Runtime warning occurred"
```

This script generates sample data with three clusters and calculates the Davies-Bouldin score using the `davies_bouldin_score` function from scikit-learn. If a runtime warning occurs during the calculation (i.e., division by zero), it prints the stack trace and raises an assertion error to indicate that the issue was reproduced.