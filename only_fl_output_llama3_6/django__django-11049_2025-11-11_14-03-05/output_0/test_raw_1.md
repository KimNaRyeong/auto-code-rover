Here is the reproducer script:

```python
from django.db import models
import datetime

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

def main():
    try:
        duration = datetime.timedelta(hours=2, minutes=14)
        models.DurationField().validate_input("14:00")
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script creates a `DurationField` and tries to validate the input `"14:00"`. Since this is not in the correct format according to the issue description, it should raise an `AssertionError`. The script then prints the stack trace of the error.