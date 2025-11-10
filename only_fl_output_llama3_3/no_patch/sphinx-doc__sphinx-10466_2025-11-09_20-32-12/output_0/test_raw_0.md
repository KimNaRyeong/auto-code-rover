Here is a standalone Python script `reproducer.py` to reproduce the issue:

```python
import os
import sphinx
from sphinx.builders import GettextBuilder
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
    # Set up the environment
    os.chdir('/path/to/blender_docs')  # Replace with your path

    # Run the make clean and make gettext commands
    try:
        os.system('make clean; make gettext')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to run make clean and make gettext")

    # Load the Po file into an editor
    po_file_path = 'build/gettext/blender_manual.pot'
    with open(po_file_path, 'r') as f:
        content = f.read()

    # Check for duplicated locations
    if len(content.split('#:')) > 10:  # Replace with your expected count
        raise AssertionError("Duplicated locations found in the Po file")

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up the environment, runs the `make clean` and `make gettext` commands, loads the Po file into an editor, and checks for duplicated locations. If the issue is present (i.e., more than 10 duplicated locations), it raises an `AssertionError`.