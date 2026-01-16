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

def test_calibrated_classifier_cv_with_pandas_output():
    import numpy as np
    from sklearn import set_config
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.exceptions import NotFittedError
    from sklearn.linear_model import SGDClassifier

    set_config(transform_output="pandas")

    model = CalibratedClassifierCV(SGDClassifier(), method='isotonic')

    try:
        model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
        predictions = model.predict(np.arange(90).reshape(30, -1))
        assert predictions is not None, "Prediction should not be None"
    except ValueError as e:
        print_stacktrace(e)
        assert False, "ValueError raised"
    except Exception as e:
        print_stacktrace(e)
        assert False, f"Unexpected exception type {type(e).__name__} raised"
    finally:
        # Reset the global configuration to its default value to avoid side effects.
        set_config(transform_output="array")

if __name__ == "__main__":
    try:
        test_calibrated_classifier_cv_with_pandas_output()
    except AssertionError as ae:
        print_stacktrace(ae)
        # Print a specific message indicating the nature of the failure
        print("\nFailed due to an AssertionError indicating the issue is present.")
        raise SystemExit(1)
    except Exception as e:
        print("\nAn unexpected error occurred:", str(e))
        raise SystemExit(1)
    else:
        print("\nTest passed; the issue does not manifest with the current configuration.")
        sys.exit(0)
```