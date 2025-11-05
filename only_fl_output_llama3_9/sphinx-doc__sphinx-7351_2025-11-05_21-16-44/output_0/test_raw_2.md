Here is a revised reproducer script that should reproduce the issue:

```python
import os
from sphinx.application import SphinxApplication
from myst_parser.parser import Parser

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
    app.config.master_doc = 'index.rst'

    parser = Parser(app, 'md')
    parser.add_source_file('a.md')
    parser.add_source_file('a.rst')

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise

    if not os.path.exists('build/html/a.md'):
        raise AssertionError("Expected a.md to be included in the build")

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a Sphinx application, configures it to build HTML documentation, and adds two source files `a.md` and `a.rst`. When the script is run, it attempts to build the documentation. If the issue is present (i.e., only one file is parsed), an `AssertionError` will be raised, and the stack trace will be printed using the `print_stacktrace` function.

To reproduce the issue, simply run the script: `python3 reproducer.py`.