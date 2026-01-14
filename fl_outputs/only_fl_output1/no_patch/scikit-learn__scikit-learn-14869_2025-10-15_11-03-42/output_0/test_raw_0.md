```python
# reproducer.py
import sys
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingClassifier

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

try:
    X = [[1, 0],
         [1, 0],
         [1, 0],
         [0, 1],
         [1, 1]]
    y = [1, 1, 1, 0, 1]
    gb = HistGradientBoostingClassifier(loss='categorical_crossentropy',
                                        min_samples_leaf=1)
    gb.fit(X, y)
    predictions = [gb.predict([[1, 0]]), gb.predict([[0, 1]])]
    
    # Asserting the output should not be as it contradicts the basics of binary classification
    assert predictions[0] == [1] and predictions[1] == [0], "HGBC with `categorical_crossentropy` fails silently on binary classification"

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```