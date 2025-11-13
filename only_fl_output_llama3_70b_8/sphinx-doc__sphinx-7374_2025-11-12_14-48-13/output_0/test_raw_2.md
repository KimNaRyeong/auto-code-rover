Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.domains.python import PythonDomain
from sphinx.directives.code import CodeBlock

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
    app = Sphinx(srcdir='.', confdir='.')
    domain = PythonDomain('test')
    directive = CodeBlock('.. py:function:: example_python_function(foo)\n\n    Some function.')
    node = directive(domain, 'test', 'example_python_function', ['foo'])
    anchor = app.builder.get_target_uri(node)
    if '-' in anchor:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a `Sphinx` application instance and uses it to parse an RST directive for a Python function with an underscore in its name. It then checks if the generated anchor uses dashes or underscores. If it uses dashes, it raises an `AssertionError` with a stack trace. If the issue is fixed, the script exits with code 0.

Please note that this script requires Sphinx to be installed and available in the Python environment where it's executed.