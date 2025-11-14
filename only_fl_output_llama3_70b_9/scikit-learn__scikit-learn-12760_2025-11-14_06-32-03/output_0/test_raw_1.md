Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn.metrics.cluster import davies_bouldin_score
from scipy.spatial.distance import pdist, euclidean

def DaviesBouldin(X, labels):
    n_cluster = len(np.bincount(labels))
    cluster_k = [X[labels == k] for k in range(n_cluster)]
    centroids = [np.mean(k, axis=0) for k in cluster_k]
    variances = [np.mean([euclidean(p, centroids[i]) for p in k]) for i, k in enumerate(cluster_k)]
    db = []

    for i in range(n_cluster):
        for j in range(n_cluster):
            if j != i:
                db.append((variances[i] + variances[j]) / euclidean(centroids[i], centroids[j]))

    return np.max(db) / n_cluster

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

def main():
    X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])
    labels = np.array([0, 0, 0, 1, 1, 1])

    try:
        sklearn_score = davies_bouldin_score(X, labels)
        stack_overflow_score = DaviesBouldin(X, labels)

        if not np.isclose(sklearn_score, stack_overflow_score):
            raise AssertionError("Scores do not match")

        # Try to reproduce the division by zero warning
        X = np.array([[1, 2], [1, 4], [1, 0]])
        labels = np.array([0, 0, 0])

        sklearn_score = davies_bouldin_score(X, labels)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue by comparing the Davies-Bouldin scores calculated using the sklearn implementation and the Stack Overflow implementation. If the scores do not match, it will raise an `AssertionError` with a stack trace of the issue.

Additionally, I added a test case to try to reproduce the division by zero warning by creating a dataset with only one cluster.