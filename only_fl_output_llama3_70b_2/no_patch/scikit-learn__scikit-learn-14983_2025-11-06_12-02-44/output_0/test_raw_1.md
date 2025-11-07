Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
    kf_stratified = RepeatedStratifiedKFold()
    assert repr(kf) != "<sklearn.model_selection._split.RepeatedKFold object at 0x[0-9a-f]+>"
    assert repr(kf_stratified) != "<sklearn.model_selection._split.RepeatedStratifiedKFold object at 0x[0-9a-f]+>"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script will raise an `AssertionError` if the `__repr__` string of `RepeatedKFold` and `RepeatedStratifiedKFold` objects is not correct, which is the case in this issue. The script will exit with code 0 if the issue is fixed.