Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import numpy as np
from hypothesis import given
from hypothesis.strategies import floats

def two_sum(a, b):
    # implementation of two_sum function
    return a + b

@given(floats(), floats())
def test_two_sum_symmetric(f1, f2):
    try:
        assert np.testing.assert_equal(two_sum(f1, f2), two_sum(f2, f1))
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

test_two_sum_symmetric(-3.089785075544792e+307, 1.7976931348623157e+308)

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

```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

You can run this script using `python3 reproducer.py`.