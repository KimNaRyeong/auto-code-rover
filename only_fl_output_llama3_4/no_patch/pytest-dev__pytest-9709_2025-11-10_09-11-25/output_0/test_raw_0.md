Here is the reproducer script:

```python
import pytest
import numpy as np

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
    a = 2**np.arange(12)
    b = 2**np.arange(12)
    np.random.shuffle(a)

    print(*set(a))
    print(*set(b))

    assert set(a) == pytest.approx(set(b))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not reproduced")
        exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace. If the issue is fixed, it will simply print "Issue not reproduced" and exit with code 0.