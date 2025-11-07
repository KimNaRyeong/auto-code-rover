Here is the reproducer script:

```python
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import unittest

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

class TestHistGradientBoostingClassifier(unittest.IsolatedTestCase):
    def test_binary_classification(self):
        X = [[1, 0], [1, 0], [1, 0], [0, 1], [1, 1]]
        y = [1, 1, 1, 0, 1]
        gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
        gb.fit(X, y)

        pred = gb.predict([[1, 0]])
        self.assertEqual(pred[0], 1, "Prediction is incorrect")

        pred = gb.predict([[0, 1]])
        self.assertEqual(pred[0], 0, "Prediction is incorrect")

    def test_binary_classification_with_stacktrace(self):
        try:
            X = [[1, 0], [1, 0], [1, 0], [0, 1], [1, 1]]
            y = [1, 1, 1, 0, 1]
            gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
            gb.fit(X, y)

            pred = gb.predict([[1, 0]])
            print_stacktrace(AssertionError("Expected prediction to be different"))
        except AssertionError as e:
            print_stacktrace(e)
            self.fail("Expected prediction to be different")

if __name__ == "__main__":
    unittest.main()
```

This script will run the tests and if the issue is present, it will raise an `AssertionError` with a stack trace.