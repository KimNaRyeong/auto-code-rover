Here is the reproducer script:

```python
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
import traceback
import sys

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

try:
    X = np.array([[1, 0], [1, 0], [1, 0], [0, 1], [1, 1]])
    y = np.array([1, 1, 1, 0, 1])
    gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
    gb.fit(X, y)
    predicted = gb.predict([[1, 0]])
    if predicted[0] != 1:
        raise AssertionError("Expected the model to predict 1 for input [[1, 0]]")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced. All tests passed.")
exit(0)
```

This script reproduces the issue by training a HistGradientBoostingClassifier with categorical cross-entropy loss on a binary classification problem and then checking if the predicted output is correct. If the prediction is incorrect, it raises an AssertionError.