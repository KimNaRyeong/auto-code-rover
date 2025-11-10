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

print("Reproducing AdaBoostClassifier 'base_estimator' deprecation issue...")

try:
    from sklearn.ensemble import AdaBoostClassifier
    clf = AdaBoostClassifier(base_estimator=None)
    clf.fit([[1]], [0])
    print("Issue is fixed!")
except Exception as e:
    print_stacktrace(e)
    assert False, "AdaBoostClassifier 'base_estimator' deprecation issue is present"
