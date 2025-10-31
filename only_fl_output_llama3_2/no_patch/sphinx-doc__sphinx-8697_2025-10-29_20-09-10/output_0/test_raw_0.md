Here is the reproducer script:

```python
import os
from sphinx import application, builder
from sphinx.util import logging

def main():
    app = application.Sphinx()
    app.builder = builder.DirectoryBuilder(app, 'source', '_build/html')

    source_dir = 'source'
    build_dir = '_build/html'

    index_rst_file = os.path.join(source_dir, 'index.rst')
    downloads_dir = os.path.join(source_dir, 'downloads')

    with open(index_rst_file, 'w') as f:
        f.write('''
#!rest

:download:`downloads/archive.zip`
:download:`/document/downloads/archive.zip`
:download:`../document/downloads/archive.zip`
''')

    app.build()

    expected_files = ['archive.zip']
    actual_files = os.listdir(os.path.join(build_dir, '_downloads'))

    if set(actual_files) != set(expected_files):
        raise AssertionError("Expected files: {}, Actual files: {}".format(expected_files, actual_files))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
```

This script creates a Sphinx application, builds the documentation, and then checks if the expected files are present in the build directory. If not, it raises an `AssertionError` with the stack trace of the issue.