Here is the revised `reproducer.py` file to reproduce the issue:
```python
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

def main():
    try:
        kf = RepeatedKFold()
        kf_stratified = RepeatedStratifiedKFold()
        assert "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)" == repr(kf)
        assert "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)" == repr(kf_stratified)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script should raise an `AssertionError` when the issue is present, and exit with code 0 when the issue is fixed.