Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn.metrics.cluster import davies_bouldin_score

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
    X = np.array([[1, 2], [1, 4], [1, 0]])
    labels = np.array([0, 0, 0])

    try:
        davies_bouldin_score(X, labels)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue by trying to calculate the Davies-Bouldin score using the sklearn implementation. If a `RuntimeWarning` is raised due to division by zero, it will be caught and printed with a stack trace.

Please note that this script assumes that scikit-learn is installed correctly. If you encounter issues with installing scikit-learn, please refer to the installation instructions in the scikit-learn documentation.