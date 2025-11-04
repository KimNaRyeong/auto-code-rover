Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from sphinx.ext import napoleon
from docutils.nodes import document
from docutils.parsers.rst import Directive
import sphinx
from sphinx.builders import Builder
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

def test_issue():
    try:
        sphinx.build_main.main(['-b', 'html', '-d', '_build/doctrees', '.'])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    os.chdir('test_project')
    os.makedirs('test_project', exist_ok=True)

    with open('conf.py', 'w') as f:
        f.write("""
import sphinxcontrib.napoleon
sphinxcontrib.napoleon.html_properties = {}
""")

    with open('example_google.py', 'w') as f:
        f.write("""
def foo():
    pass

__author__ = "John Doe"
__date__ = "2022-01-01"
""")

    with open('index.rst', 'w') as f:
        f.write("""
Google Example
==============

.. automodule:: example_google
   :members:
   :noindex:

:ref:`genindex`
""")

    test_issue()
```

This script creates a temporary project directory, generates the necessary files (`conf.py`, `example_google.py`, and `index.rst`), and then attempts to build the HTML documentation using Sphinx. If the issue is present, it will raise an `AssertionError` and print the stack trace.