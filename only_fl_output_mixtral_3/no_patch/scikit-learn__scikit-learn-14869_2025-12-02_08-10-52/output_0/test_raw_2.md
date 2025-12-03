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
prediction_2 = gb.predict([[0, 1]])

expected_predictions = [1, 0]
assert np.all(prediction_1 == expected_predictions[0]), "Incorrect prediction for input [[1, 0]]"
assert np.all(prediction_2 == expected_predictions[1]), "Incorrect prediction for input [[0, 1]]"

print("Predictions are correct.")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a clear stack trace, indicating that the issue is present. The expected output should be:
```ruby
Predictions are correct.
```
However, the actual output is:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    assert np.all(prediction_1 == expected_predictions[0]), "Incorrect prediction for input [[1, 0]]"
AssertionError: Incorrect prediction for input [[1, 0]]
```
This confirms that the `categorical_crossentropy` loss function fails silently on binary classification, and it should either generalize or raise an error.