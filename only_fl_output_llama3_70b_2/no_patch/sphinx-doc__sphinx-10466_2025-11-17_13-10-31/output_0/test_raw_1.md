I apologize for the previous mistake. Here is a new standalone Python script `reproducer.py` to reproduce the issue:
```python
import os
from sphinx.application import Sphinx
from sphinx.builders.gettext import GettextBuilder

def reproducer():
    # Create a temporary directory for the build
    temp_dir = 'temp_build'
    os.makedirs(temp_dir, exist_ok=True)

    # Initialize Sphinx application
    app = Sphinx(srcdir='.', confdir='.', outdir=temp_dir)
    app.buildername = 'gettext'

    # Create a GettextBuilder instance
    builder = GettextBuilder(app)

    # Process the documentation sources
    builder.build_all()

    # Load the generated .pot file
    pot_file_path = os.path.join(temp_dir, 'blender_manual.pot')
    with open(pot_file_path, 'r') as f:
        pot_content = f.read()

    # Check for duplicated locations
    lines = pot_content.splitlines()
    locations = [line[3:] for line in lines if line.startswith('#: ')]
    unique_locations = set(locations)
    if len(unique_locations) != len(locations):
        raise AssertionError("Duplicated locations found in .pot file")

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
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a temporary directory for the build, initializes a Sphinx application with the `gettext` builder, processes the documentation sources, loads the generated `.pot` file, and checks for duplicated locations. If duplicated locations are found, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the issue.

Please make sure that you have Sphinx installed in your Python environment before running this script.