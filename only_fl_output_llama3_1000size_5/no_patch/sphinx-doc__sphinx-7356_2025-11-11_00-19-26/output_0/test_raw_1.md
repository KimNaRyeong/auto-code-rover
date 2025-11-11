I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
from docutils import nodes
from docutils.parsers.rst import Directive
import sphinx
from sphinx.util import logging

def setup_sphinx():
    sphinx.domains.python.setup()

def test_python_domain_ids():
    rst = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    from io import StringIO
    from docutils.core import publish_string
    
    output = publish_string(rst, writer_name='html')
    
    if "example-python-function" in output.decode('utf-8'):
        raise AssertionError("Expected 'example_python_function' but got 'example-python-function'")

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

if __name__ == "__main__":
    try:
        test_python_domain_ids()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up the Sphinx domain for Python, then uses the `publish_string` function to process a piece of RST that defines a Python function. It checks if the generated HTML contains the expected fragment identifier (`#example_python_function`) or the new one (`#example-python-function`). If it finds the new one, it raises an `AssertionError`.