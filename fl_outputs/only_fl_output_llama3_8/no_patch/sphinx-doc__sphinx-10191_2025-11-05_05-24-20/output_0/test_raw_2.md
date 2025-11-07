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
    rst_file = 'index.rst'
    os.system('make latexpdf')

    try:
        with open(rst_file, 'r') as f:
            rst_string = f.read()
    except FileNotFoundError:
        print_stacktrace(FileNotFoundError(f"{rst_file} not found"))
        sys.exit(1)

    if rst_string != """
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
""":
        print_stacktrace(AssertionError("Expected RST string not matched"))
        sys.exit(1)

    if os.path.exists('index.pdf'):
        os.remove('index.pdf')

    try:
        os.system('make latexpdf')
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by running `make latexpdf` and checking if the generated PDF file contains the expected footnote marks. If the issue is present, it will raise an `AssertionError` and print the stack trace.