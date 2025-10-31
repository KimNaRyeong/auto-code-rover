Here is the reproducer script:

```python
import os
import sys
from sphinx.application import SphinxApplication
from sphinx.util import logging

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
    app = SphinxApplication()
    app.config.linkcheck_anchors = True
    try:
        from sphinx.cmd import make_linkcheck_file
        make_linkcheck_file(['source/index.rst'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a Sphinx application with `linkcheck_anchors` set to True, then attempts to build the index.rst file using the linkcheck builder. If an exception is raised during this process (which should happen when the server returns an HTTP error), it prints the stack trace and raises an AssertionError if the issue is not reproduced.