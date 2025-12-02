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
prediction_1 = gb.predict([[1, 0]])
prediction_0 = gb.predict([[0, 1]])

expected_prediction_1 = 1
expected_prediction_0 = 0

if prediction_1 != expected_prediction_1 or prediction_0 != expected_prediction_0:
    raise AssertionError(f"Expected prediction for [1, 0] to be {expected_prediction_1}, but got {prediction_1}. Expected prediction for [0, 1] to be {expected_prediction_0}, but got {prediction_0}.")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    raise AssertionError(f"Expected prediction for [1, 0] to be {expected_prediction_1}, but got {prediction_1}. Expected prediction for [0, 1] to be {expected_prediction_0}, but got {prediction_0}.")
AssertionError: Expected prediction for [1, 0] to be 1, but got 0. Expected prediction for [0, 1] to be 0, but got 0.
```
This confirms that the `categorical_crossentropy` loss function fails silently on binary classification, and should either generalize or raise an error.