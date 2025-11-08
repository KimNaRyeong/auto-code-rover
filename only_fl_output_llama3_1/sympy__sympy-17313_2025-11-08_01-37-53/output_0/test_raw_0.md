Here is the reproducer script:

```python
import math

def floor(x):
    return int(math.floor(x))

def ceiling(x):
    return int(math.ceil(x))

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
    assert ceiling(1) > 0
    assert floor(-1) < 0
    assert floor(1) >= 0
    assert ceiling(-1) <= 0
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue fixed!")
    exit(0)
```

This script defines the `floor` and `ceiling` functions, then attempts to run assertions on these functions. If any of the assertions fail, it prints a stack trace using the provided function and exits with code 1. If all assertions pass, it prints "Issue fixed!" and exits with code 0.