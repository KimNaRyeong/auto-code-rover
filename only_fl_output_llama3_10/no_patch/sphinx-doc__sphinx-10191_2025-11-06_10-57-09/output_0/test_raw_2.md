Here is the reproducer script:

```python
import os
from docutils.core import publish_string
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

def reproduce_issue():
    rst_content = """
Test
====

Explicitly numbered footnotes
-----------------------------

First reference to first footnote [1]_ 

First reference to second footnote [2]_]

Second reference to first footnote [1]_

Second reference to second footnote [2]_]"

    try:
        output = publish_string(rst_content, writer_name='latex')
        if "?\n" in output:
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script uses the `publish_string` function from the `docutils.core` module to generate a LaTeX document from the given RST content. If the issue is present, it raises an `AssertionError`.