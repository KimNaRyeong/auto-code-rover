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
    kf = RepeatedKFold()
    assert repr(kf) == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)"
    kf_stratified = RepeatedStratifiedKFold()
    assert repr(kf_stratified) == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script creates instances of `RepeatedKFold` and `RepeatedStratifiedKFold`, and then checks if their `__repr__` strings match the expected results. If they don't, it raises an `AssertionError`, prints a stack trace using the provided function, and exits with code 1. If the issue is fixed, the script exits with code 0.