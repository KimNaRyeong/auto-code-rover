Here is the reproducer script:

```python
import sys
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold
from sklearn.utils.testing import assert_raises

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

def reproduce_issue():
    try:
        assert repr(RepeatedKFold()) == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)"
        assert repr(RepeatedStratifiedKFold()) == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will execute the `repr` function on both `RepeatedKFold` and `RepeatedStratifiedKFold`, and then assert that the result is equal to the expected string. If the assertion fails, it will print a stack trace of the failure and exit with code 1.