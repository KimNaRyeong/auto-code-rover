Based on your requirements and the previous context, here is a `reproducer.py` script designed to reproduce the issue while clearly printing a stack trace for any exception caught during execution. This script attempts to create conditions for the issue related to `CalibratedClassifierCV` not working properly with `set_config(transform_output="pandas")` set, specifically when using isotonic regression. Here is how you could achieve that:

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

def main():
    import numpy as np
    from sklearn import set_config
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.linear_model import SGDClassifier

    # Force output transformation to pandas DataFrame
    set_config(transform_output="pandas")

    model = CalibratedClassifierCV(SGDClassifier(), method='isotonic')

    try:
        model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
        predictions = model.predict(np.arange(90).reshape(30, -1))
        # If the prediction succeeds, we assert False as the issue should've caused a crash
        assert False, "Successfully predicted without errors."
    except ValueError as e:
        print_stacktrace(e)
        # Validate the type of error to ensure it's due to the issue in question
        if "could not broadcast input array from shape" in str(e):
            print("The issue is successfully reproduced.")
        else:
            raise AssertionError("An error occurred, but it doesn't match the expected issue.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred which doesn't match the expected issue.")

if __name__ == "__main__":
    main()
```

This script will attempt to reproduce the issue described. Upon running, it should print out a detailed stack trace if the exception is caught due to the described bug (i.e., due to the inability of `CalibratedClassifierCV` to handle `pandas` DataFrame output with isotonic regression). If the execution passes without any exceptions caught, which is highly unlikely given the script's design, it would misleadingly assert that the prediction succeeded without errors. Hence, the design primarily focuses on catching and asserting the specific error related to the issue at hand.