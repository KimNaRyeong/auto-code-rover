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
    from sklearn.dummy import DummyClassifier
    try:
        clf = DummyClassifier(strategy='constant', constant='not-in-dataset')
        clf.fit([[1., 2.]], ['class1'])
    except ValueError as e:
        expected_error_msg = "The constant target value must be present in the training data.\nYou provided: constant='not-in-dataset'. Possible values are: ['class1']."
        # Check the original error message
        original_error_msg = "The constant target value must be present in training data"
        if original_error_msg in str(e):
            print_stacktrace(e)
            # Check if the improved message is already in place
            assert expected_error_msg not in str(e), "The issue seems to be fixed!"
        else:
            # If the error message is already improved.
            assert expected_error_msg in str(e), "Error message is not as expected even after the fix."
            print("The issue has been resolved.")

if __name__ == '__main__':
    main()
```

In this script, `main` is executed when the script is run. It tries to fit a `DummyClassifier` from scikit-learn with a constant strategy using a constant value that is not present in the dataset, which is expected to raise a `ValueError`. The catch block checks if the error message is the original one, indicating the issue is present, then it prints a stack trace with a custom function `print_stacktrace`. If the original error message is not detected and the new, improved error message is present instead, it indicates the issue has been resolved.