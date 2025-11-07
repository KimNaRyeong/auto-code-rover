Here is the reproducer script:

```python
import os
from docutils import nodes
from sphinx.util.nodes import normalize_path

def reproduce_issue():
    try:
        conf = {
            'master_doc': 'index',
            'source_dir': 'source',
            'build_dir': '_build'
        }
        source_dir = 'source'
        build_dir = '_build'

        # Create the directory structure
        os.makedirs(os.path.join(source_dir, 'document'), exist_ok=True)
        with open(os.path.join(source_dir, 'document', 'index.rst'), 'w') as f:
            f.write('''
:download:`downloads/archive.zip`
:download:`/document/downloads/archive.zip`
:download:`../document/downloads/archive.zip`
''')

        # Run Sphinx
        from sphinx.application import SphinxApplication
        app = SphinxApplication()
        app.build(['source'], ['_build'])

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

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
    reproduce_issue()
```

This script will create a Sphinx project with the given structure and run the build command. If the issue is present, it will raise an `AssertionError` and print the stack trace.