Here is the reproducer script in a code block:

```python
import pytest
from decimal import Decimal

def test_approx_decimal():
    actual = [Decimal("1.000001"), Decimal("2.000001")]
    expected = [Decimal("1"), Decimal("2")]

    with pytest.raises(AssertionError):
        assert actual == pytest.approx(expected)

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
    test_approx_decimal()
except AssertionError as e:
    print_stacktrace(e)
```

This script will raise an `AssertionError` when the issue is present, and it will print a stack trace of the issue.