Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
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

def reproduce_issue():
    app = SphinxApplication()
    app.builder = 'html'
    app.config.master_doc = 'index'

    from sphinx.util import logging
    logging.getLogger().setLevel(logging.INFO)

    with open('index.rst', 'w') as f:
        f.write('''
Indices
--------

* _@_ entry 1
* normal word
* _£_ entry 2
* another normal word
* _←_ entry 3

''')

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a simple Sphinx project with an `index.rst` file containing the problematic index entries. It then attempts to build the HTML documentation using Sphinx's `build()` method. If the issue is present, it prints the stack trace and raises an `AssertionError`.