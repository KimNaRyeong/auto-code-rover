import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    import sklearn
    from sklearn.dummy import DummyClassifier
    clf = DummyClassifier(strategy='constant', constant='not-in-dataset')
    clf.fit([[1., 2.]], ['class1'])
except ImportError as e:
    print_stacktrace(e)
    assert False, "Scikit-learn is not installed correctly"
except ValueError as e:
    if str(e) == "The constant target value must be present in training data.":
        print_stacktrace(e)
        assert False, "Error should be improved with DummyClassifier constant strategy when constant value not in training data"
    else:
        raise
