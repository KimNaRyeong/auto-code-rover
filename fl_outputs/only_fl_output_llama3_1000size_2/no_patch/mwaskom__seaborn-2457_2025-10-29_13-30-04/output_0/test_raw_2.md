Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
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

def main():
    try:
        with redirect_stdout(StringIO()):
            sns.lineplot(x=[1, 1, 2, 2], y=[1, 2, 3, 4], ci=None)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(0)
    else:
        print("Issue not found. Exiting with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script should reproduce the issue by calling `sns.lineplot` with `ci=None`.