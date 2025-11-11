Here is the reproducer script:

```python
import math
import sys
from typing import Any

def print_stacktrace(e: Exception) -> None:
    """Prints a stack trace with line numbers"""
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue() -> None:
    try:
        result = math.floor(2 / .5)
        assert result == 4, "Expected 4 but got {}".format(result)
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function `reproduce_issue` when executed. The function attempts to divide 2 by 0.5, which should raise a ZeroDivisionError. If an exception is raised, it prints the stack trace using the provided function and then raises the same exception again. If no exception is raised (i.e., the issue is fixed), it exits with code 0.