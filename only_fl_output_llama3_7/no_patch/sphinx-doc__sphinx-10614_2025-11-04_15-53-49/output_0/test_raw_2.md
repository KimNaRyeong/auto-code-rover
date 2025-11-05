Here is a standalone Python script to reproduce the issue:

```python
import os
from sphinx.ext import inheritance_diagram
from sphinx.application import SphinxApplication

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
    try:
        app.builder = inheritance_diagram.InheritanceDiagramBuilder()
        app.build('docs_source', 'docs_build')
        os.chdir('docs_build')
        with open('index.html') as f:
            content = f.read()
        if not content.startswith('<svg'):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    reproduce_issue()
```

This script will create a Sphinx application, build the inheritance diagram for `docs_source` and `docs_build`, change to the `docs_build` directory, read the content of `index.html`, and check if it starts with `<svg`. If not, an `AssertionError` is raised.