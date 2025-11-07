```python
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

def test_categorical_crossentropy_with_binary_classification():
    import numpy as np
    from sklearn.experimental import enable_hist_gradient_boosting # noqa
    from sklearn.ensemble import HistGradientBoostingClassifier

    X = np.array([[1, 0],
                  [1, 0],
                  [1, 0],
                  [0, 1],
                  [1, 1]])
    y = np.array([1, 1, 1, 0, 1])
    gb = HistGradientBoostingClassifier(loss='categorical_crossentropy',
                                        min_samples_leaf=1)
    try:
        gb.fit(X, y)
        predictions = gb.predict([[1, 0], [0, 1]])
        assert predictions[0] == 1 and predictions[1] == 0, \
            "Model trained with 'categorical_crossentropy' incorrectly predicts binary classification."
    except ValueError as e:
        print_stacktrace(e)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_categorical_crossentropy_with_binary_classification()
```