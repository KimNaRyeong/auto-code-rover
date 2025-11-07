Here is the reproducer script:

```python
import os
from docutils.core import publish_string
from io import StringIO
from sphinx.application import SphinxApplication
from sphinx.util.docset import DocSet

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
    app = SphinxApplication()
    docset = DocSet(app)
    try:
        app.build_string('latex', rst_string, 'index')
        if '?' in open('index.tex').read():
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script uses the `sphinx` library to build a LaTeX document from an RST string. It checks if the generated LaTeX file contains a '?' character, which should indicate the presence of the issue. If the issue is present, it raises an `AssertionError`.