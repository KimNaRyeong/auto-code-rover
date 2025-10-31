Here is the reproducer script:

```python
import os
from docutils.core import publish_string
from io import StringIO

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
        output = publish_string(rst_string, writer_name='latex')
        if '?' in output.decode('utf-8'):
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script uses the `docutils` library to publish an RST string to LaTeX. It checks if the output contains a '?' character, which should indicate the presence of the issue. If the issue is present, it raises an `AssertionError`.