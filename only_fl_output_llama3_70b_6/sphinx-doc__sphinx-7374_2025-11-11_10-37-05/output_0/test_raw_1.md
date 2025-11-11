Here is a new standalone Python script `reproducer.py` to reproduce the issue:
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
    html = publish_string(rst_content, writer=HTMLTranslator()).decode('utf-8')
    if '#example-python-function' in html:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")
    elif '#example_python_function' not in html:
        print("The issue is fixed!")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script uses the `docutils` library to generate HTML from a simple reStructuredText document containing a Python function with an underscore in its name. It then checks if the generated HTML file contains the expected anchor ID. If it doesn't, it raises an `AssertionError` with a stack trace.

Please note that this script requires the `docutils` library to be installed. You can install it using `pip install docutils`.