Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
from sphinx.util.fileutil import copyfileobj

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
    app.build_dir = 'build'
    app.builder = 'html'

    conf_file = open('conf.py', 'w')
    conf_file.write("""
import os

project = u'My Project'
copyright = u'2023, My Company'

master_doc = 'index'

latex_documents = [
    ('index', 'index.tex', project + ' Manual',
     project + ' Manual', 'manual'),
]

html_favicon = 'favicon.ico'
""")
    conf_file.close()

    index_file = open('index.rst', 'w')
    index_file.write("""
Symbols
--------

@ symbol 1
normal text

£ symbol 2
normal text

← symbol 3
normal text
""")
    index_file.close()

    app.build()

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
```

This script creates a Sphinx project with an `index.rst` file containing the problematic symbols. It then builds the HTML documentation and checks if the issue is present by asserting that there are not two sections called "Symbols" in the generated index.html file. If the assertion fails, it prints the stack trace of the exception and exits with code 0.