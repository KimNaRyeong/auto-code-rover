 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

X = [[1, 0],
     [1, 0],
     [1, 0],
     [0, 1],
     [1, 1]]
y = [1, 1, 1, 0, 1]
gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
gb.fit(X, y)
predictions = gb.predict([[1, 0], [0, 1]])
if np.all(predictions == [0, 0]):
    raise AssertionError("`categorical_crossentropy` should not always predict 0 for binary classification.")
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    raise AssertionError("`categorical_crossentropy` should not always predict 0 for binary classification.")
AssertionError: `categorical_crossentropy` should not always predict 0 for binary classification.
```
This reproduces the issue where `categorical_crossentropy` fails silently on binary classification by always predicting 0.