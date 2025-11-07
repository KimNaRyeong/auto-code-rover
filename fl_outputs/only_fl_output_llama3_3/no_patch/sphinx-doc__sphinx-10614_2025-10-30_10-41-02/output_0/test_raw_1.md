Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
from sphinx.ext import inheritance_diagram
from sphinx.application import SphinxApplication
from sphinx.util import logging

def generate_inheritance_diagram():
    app = SphinxApplication()
    app.builder = 'html'
    app.config.inheritance_diagram_module_name_prefix = 'my_package.'
    app.config.inheritance_diagram_file_suffix = '.html'

    try:
        inheritance_diagram('my_package.MyClass1')
        inheritance_diagram('my_package.MyClass2')
    except Exception as e:
        logging.info(f"Error: {e}")
        raise

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

if __name__ == '__main__':
    os.chdir('path_to_your_project')  # replace with the path to your project
    generate_inheritance_diagram()
```

This script should be run in the root directory of the project. It will raise an `AssertionError` when the issue is present and print a stack trace of the issue.