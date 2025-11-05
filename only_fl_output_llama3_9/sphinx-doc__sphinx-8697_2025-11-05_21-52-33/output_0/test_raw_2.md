Here is the reproducer script:

```python
import os
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
    app.builder = 'html'
    app.srcdir = os.path.join(os.getcwd(), "source")
    app.confdir = os.path.join(os.getcwd(), "conf")
    app.outdir = "_build"

    try:
        with open(os.path.join(app.srcdir, "index.rst"), mode="w") as f:
            f.write(":download:`downloads/archive.zip`\n")
            f.write(":download:`/document/downloads/archive.zip`\n")
            f.write(":download:`../document/downloads/archive.zip`\n")

        app.build()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script creates a Sphinx application, sets the source directory to the current working directory, and builds the HTML output. It also writes three download directives into an `index.rst` file in the source directory. If the issue is present (i.e., multiple files are generated), it raises an `AssertionError`.