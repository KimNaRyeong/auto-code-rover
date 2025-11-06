Here is the reproducer script:

```python
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import unittest

class TestHistGradientBoostingClassifier(unittest.IsolatedTestCase):
    def test_binary_classification(self):
        X, y = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_classes=2)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

        gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
        gb.fit(X_train, y_train)

        pred = gb.predict(X_test)
        accuracy = accuracy_score(y_test, pred)
        report = classification_report(y_test, pred)

        self.assertGreater(accuracy, 0.5, "Accuracy is too low")
        self.assertIn("1.00", str(report), "Report does not contain the expected accuracy")

    def test_binary_classification_with_prediction(self):
        X = [[1, 0], [1, 0], [1, 0], [0, 1], [1, 1]]
        y = [1, 1, 1, 0, 1]
        gb = HistGradientBoostingClassifier(loss='categorical_crossentropy', min_samples_leaf=1)
        gb.fit(X, y)

        pred = gb.predict([[1, 0]])
        self.assertEqual(pred[0], 1, "Prediction is incorrect")

        pred = gb.predict([[0, 1]])
        self.assertEqual(pred[0], 0, "Prediction is incorrect")

    def test_binary_classification_with_prediction_and_stacktrace(self):
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