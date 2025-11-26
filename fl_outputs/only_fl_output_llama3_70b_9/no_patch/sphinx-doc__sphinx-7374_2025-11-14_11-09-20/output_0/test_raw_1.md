Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.parsers.rst import Directive, directives
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
    domain = PythonDomain('test')
    directive = Directive('py:function', ['example_python_function'])
    node = domain.create_object('function', 'example_python_function', 0, '')
    
    if '#' + '-'.join(node['ids'][0].split('_')) != '#example-python-function':
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
This script creates a PythonDomain object and uses it to create an object for a Python function with an underscore in its name. It then checks if the ID of the created node is using dashes instead of underscores. If it does, it raises an `AssertionError` with a stack trace. If not, it prints a success message and exits with code 0.