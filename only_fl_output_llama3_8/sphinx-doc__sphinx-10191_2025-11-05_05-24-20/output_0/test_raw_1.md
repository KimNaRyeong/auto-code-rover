Here is the reproducer script:

```python
import os
from docutils.core import publish_string
import sys
import traceback

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
    rst_string = """
Test
====

Explicitly numbered footnotes
-----------------------------

First reference to first footnote [1]_

First reference to second footnote [2]_

Second reference to first footnote [1]_

Second reference to second footnote [2]_

.. rubric:: Footnotes

.. [1] A first footnote

.. [2] A second footnote
"""

    try:
        publish_string(rst_string, writer_name='latex')
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not reproduced. All good!")
        sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to publish the given RST string using Sphinx's `publish_string` function, which should reproduce the issue if it exists. If an `AssertionError` is raised during the execution of the script, it will print the stack trace and exit with code 1.