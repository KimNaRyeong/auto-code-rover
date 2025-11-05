Here is the reproducer script:

```python
import os
import sys
from sphinx.application import SphinxApplication
from sphinx.util import logging
from io import StringIO
import subprocess

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
    os.chdir('path_to_your_project')  # replace with your project path
    app = SphinxApplication()
    app.config.linkcheck_anchors = True

    try:
        output = subprocess.check_output(['make', 'linkcheck'], stderr=subprocess.PIPE)
        if "404 Client Error: Not Found" not in str(output.decode('utf-8')):
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script changes the directory to your project, sets `linkcheck_anchors` to `True`, runs the `make linkcheck` command and checks if the output contains "404 Client Error: Not Found". If not, it raises an `AssertionError`.