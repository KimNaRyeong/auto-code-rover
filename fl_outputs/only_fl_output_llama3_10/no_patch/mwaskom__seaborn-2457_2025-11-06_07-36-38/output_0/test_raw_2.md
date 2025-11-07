Here is the reproducer script:

```python
import seaborn as sns
from io import StringIO
from contextlib import redirect_stdout
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    try:
        with redirect_stdout(StringIO()):
            sns.lineplot(x=[1, 1, 2, 2], y=[1, 2, 3, 4], ci=None)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_issue()
```

This script will attempt to reproduce the issue by calling `sns.lineplot` with `ci=None`. If an assertion error is raised, it will print the stack trace and then re-raise the exception.