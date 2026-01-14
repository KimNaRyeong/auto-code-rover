 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.exceptions import NotImplementedError

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Create a synthetic dataset for classification
    trainX, trainY = make_classification(n_samples=100, n_features=20, n_classes=2)

    # Create an AdaBoostClassifier with the "SAMME" algorithm and SVC as the base estimator
    ada = AdaBoostClassifier(algorithm="SAMME", base_estimator=SVC())

    # Fit the model to the training data
    ada.fit(trainX, trainY)

    # Attempt to get probability estimates for the test data
    try:
        ada.predict_proba(trainX)
    except NotImplementedError as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should print the following stack trace and exit with code 1:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 33, in <module>
    main()
  File "reproducer.py", line 28, in main
    ada.predict_proba(trainX)
  File "/Library/Python/2.7/site-packages/sklearn/ensemble/weight_boosting.py", line 717, in predict_proba
    for estimator, w in zip(self.estimators_,
  File "/Library/Python/2.7/site-packages/sklearn/ensemble/weight_boosting.py", line 718, in <genexpr>((estimator, w))
    self.estimator_weights_))
  File "/Library/Python/2.7/site-packages/sklearn/svm/base.py", line 495, in predict_proba
    raise NotImplementedError(
NotImplementedError: probability estimates must be enabled to use this method
```
This script uses the `make_classification` function from `sklearn.datasets` to generate a synthetic dataset for classification. It then creates an `AdaBoostClassifier` with the "SAMME" algorithm and SVC as the base estimator, fits the model to the training data, and attempts to get probability estimates for the training data. The `try-except` block catches the `NotImplementedError` exception and prints the stack trace using the `print_stacktrace` function. Finally, the script asserts that the issue has been reproduced and exits with code 1.