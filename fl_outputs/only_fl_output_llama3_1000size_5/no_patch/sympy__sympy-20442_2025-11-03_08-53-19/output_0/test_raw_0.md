Here is the reproducer script:

```python
import sympy as sp
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

def reproduce_issue():
    try:
        sp.convert_to(sp.joule*sp.second, sp.joule)
    except Exception as e:
        f = StringIO()
        with redirect_stdout(f):
            print_stacktrace(e)
        print(f.read(), flush=True)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to convert `joule*second` to `joule`. If the issue is present, it will catch the exception and print the stack trace.