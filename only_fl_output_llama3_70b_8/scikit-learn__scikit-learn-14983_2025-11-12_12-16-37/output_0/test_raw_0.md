Here is the `reproducer.py` file:
```
import sys
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    assert repr(RepeatedKFold()) == 'RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)'
    assert repr(RepeatedStratifiedKFold()) == 'RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)'
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script will raise an `AssertionError` if the `__repr__` strings of `RepeatedKFold` and `RepeatedStratifiedKFold` are not as expected, and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.