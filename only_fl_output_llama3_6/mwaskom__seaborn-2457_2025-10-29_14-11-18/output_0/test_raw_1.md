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
        sns.set()
        f = StringIO()
        with redirect_stdout(f):
            sns.lineplot(x=[1, 1, 2, 2], y=[1, 2, 3, 4], ci=None)
        output = f.getvalue().strip()
        if "errorbar" not in output:
            raise AssertionError("Expected 'ci=None' to be ignored and reformatted as 'errorbar=None'")
    except Exception as e:
        print_stacktrace(e)
        raise
    if "errorbar" not in output:
        sys.exit(0)

if __name__ == "__main__":
    test_issue()
```

This script sets up a test case that attempts to create a line plot with `ci=None`. If the issue is present, it will print the stack trace and exit with code 1. If the issue is fixed, it will exit with code 0.