Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.parsers.rst import Directive, directives
from sphinx.domains.python import PythonDomain
from sphinx.application import Sphinx

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
    app = Sphinx(srcdir='', confdir='', outdir='')
    domain = PythonDomain('test')
    app.add_domain(domain)
    
    rst_text = """.. py:function:: example_python_function(foo)

    Some function."""
    doc = app.parser.parse(rst_text, '')
    app.env.resolve_references(doc, app.builder, doc)
    
    if '#' + '-'.join(doc[0][1].split('_')) != '#example-python-function':
        print("Issue is fixed")
        exit(0)
    else:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a Sphinx application and adds the PythonDomain to it. It then parses an RST document with a Python function directive, resolves references, and checks if the ID of the created node is using dashes instead of underscores. If it does, it raises an `AssertionError` with a stack trace. If not, it prints a success message and exits with code 0.