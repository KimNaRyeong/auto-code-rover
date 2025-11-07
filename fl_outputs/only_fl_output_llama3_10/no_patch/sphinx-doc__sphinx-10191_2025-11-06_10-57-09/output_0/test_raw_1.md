Here is the reproducer script:

```python
import os
from sphinx import cmdline
import sys
import subprocess
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

def reproduce_issue():
    try:
        subprocess.run(['make', 'latexpdf'], cwd=os.getcwd(), check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        if "Unknown footnote" in str(e.stdout):
            raise AssertionError("Issue reproduced")
        else:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script runs the `make latexpdf` command to build the Sphinx documentation. If the issue is present, it raises an `AssertionError`.