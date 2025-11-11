Here is the reproducer script:

```python
import mlxtend.classifier as mc
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np
import random
import unittest
from io import StringIO
import sys

class TestStacking(unittest.TestCase):

    def test_stacking(self):
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.5, random_state=random.randint(0,100))
        estimators = [('rf', RandomForestClassifier()), ('dt', mc.LogisticRegression())]
        stacking = StackingClassifier(estimators=estimators, final_estimator=RandomForestClassifier(), use_features_in_secondary=True)
        try:
            stacking.fit(X_train, y_train)
        except AssertionError as e:
            print_stacktrace(e)
            self.fail("AssertionError was expected")

    def print_stacktrace(self, e: Exception):
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

if __name__ == '__main__':
    unittest.main()
```

This script uses the `unittest` framework to test the issue. It creates a random forest and logistic regression classifier, then trains a stacking classifier using these estimators. The `use_features_in_secondary` parameter is set to `True`, which should cause an assertion error when training the final estimator.