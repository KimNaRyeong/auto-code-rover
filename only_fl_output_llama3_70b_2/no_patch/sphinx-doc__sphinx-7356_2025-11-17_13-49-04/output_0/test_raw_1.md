Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.core import publish_string
from docutils.writers.html4css1 import HTMLTranslator

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
    rst_content = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    try:
        html = publish_string(rst_content, writer_name='html')
        translator = HTMLTranslator()
        output = translator.translate(html)
        expected_anchor = 'example-python-function'
        actual_anchor = [line for line in output.splitlines() if 'href' in line][0].split('"')[1]
        assert actual_anchor == expected_anchor
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_python_domain_ids()
```
This script uses the `docutils` library to generate HTML from a reStructuredText string, and checks if the generated anchor for a Python function with an underscore in its name uses dashes instead of underscores. If the issue is present, it raises an `AssertionError` with a stack trace.