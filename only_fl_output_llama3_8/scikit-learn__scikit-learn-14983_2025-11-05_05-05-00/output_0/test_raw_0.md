Here is the reproducer script:

```python
import sys
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold
from io import StringIO
from contextlib import redirect_stdout

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

try:
    f = StringIO()
    with redirect_stdout(f):
        repr(RepeatedKFold())
        repr(RepeatedStratifiedKFold())
    output = f.getvalue().strip()
    if not (output == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)" and
            output == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"):
        raise AssertionError("Incorrect __repr__ string")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not reproduced. All tests passed.")
sys.exit(0)
```

This script will execute the `repr` function for both `RepeatedKFold` and `RepeatedStratifiedKFold`, capture the output, and check if it matches the expected string. If the issue is present (i.e., the actual output does not match the expected output), an `AssertionError` will be raised with a stack trace printed to stderr.