Certainly! Below is a standalone Python script designed to reproduce the issue described. The script includes a function to print the stack trace as required, and structure to catch the exception and print a detailed error message. This script is self-contained and should be placed at the root of your project to verify the issue.

```python
# reproducer.py

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

def test_calibrated_classifier():
    import numpy as np
    from sklearn import set_config
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.linear_model import SGDClassifier

    try:
        set_config(transform_output="pandas")
        model = CalibratedClassifierCV(SGDClassifier(), method='isotonic')
        model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
        model.predict(np.arange(90).reshape(30, -1))
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    try:
        test_calibrated_classifier()
        print("Issue has been fixed, no errors encountered.")
    except AssertionError as e:
        print(e)
        exit(1)
```

This script follows the instructions to:
1. Use sklearn's `set_config(transform_output="pandas")` before creating and fitting a `CalibratedClassifierCV`.
2. Attempt to reproduce the bug as specified, where a `ValueError` should be raised due to issues with handling output shapes.
3. Utilize the provided `print_stacktrace` function to print out detailed traceback information if an exception is encountered.
4. Exit with code `0` only if the issue is fixed, otherwise, it raises an `AssertionError` and provides a clear stack trace of the error.

To use this script, simply save it as `reproducer.py` in the root directory of your project and execute it with Python 3:

```shell
python3 reproducer.py
```

If the issue persists, the script will raise an `AssertionError`, print the stack trace, and exit with code `1`. If the issue is fixed in a future version of the libraries involved, the script will print a success message and exit with code `0`.