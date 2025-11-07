Here is a new `reproducer.py` file to reproduce the issue:
```
import os
from docutils.parsers.rst import Directive, directives
from sphinx.domains.python import PythonDomain
from sphinx.directives.code import CodeBlock
from docutils.core import publish_string

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

def test_python_domain_ids():
    rst_string = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    document = publish_string(rst_string, writer_name='html')
    if 'example-python-function' in str(document):
        raise AssertionError("Python domain IDs are using dashes instead of underscores")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script uses the `publish_string` function from `docutils.core` to parse a simple reStructuredText string containing a Python function directive. It then checks if the generated HTML output contains the anchor ID with dashes instead of underscores. If the issue is present, it raises an `AssertionError` and prints a stack trace of the issue.

Please note that this script assumes that you have Sphinx installed in your environment.