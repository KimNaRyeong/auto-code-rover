Here is a new `reproducer.py` file that reproduces the issue:
```
import os
from docutils.parsers.rst import Directive, directives
from sphinx.directives.code import CodeBlock
from sphinx.domains.python import PythonDomain

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
    domain = PythonDomain()
    directive = CodeBlock('py:function', 'example_python_function(foo)\n\n    Some function.')
    node = directive(1, '', '', 0, 0)
    anchor = domain.get_object_anchors(node)[0][1]
    
    if '-' in anchor:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")
    else:
        print("Issue is fixed")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
<|start_header_id|>