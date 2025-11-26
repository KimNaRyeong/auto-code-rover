Here is the `reproducer.py` file that reproduces the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.linkcheck import CheckExternalLinksBuilder

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

def main():
    src_dir = 'docs/source'
    out_dir = 'docs/_build/linkcheck'

    # Create a Sphinx application
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'linkcheck')

    # Register the linkcheck builder
    app.add_builder(CheckExternalLinksBuilder)

    try:
        # Build the documentation with link checking
        app.build()

        # Check if the link is broken
        with open(os.path.join(out_dir, 'index.html'), 'r') as f:
            content = f.read()
            assert 'OpenSSL\'s test vectors' in content, "Link is broken"

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Linkcheck failed")

if __name__ == '__main__':
    main()
```
This script creates a Sphinx application with the `linkcheck` builder and builds the documentation. It then checks if the link is present in the generated HTML file. If the link is broken, it raises an `AssertionError` with a stack trace of the issue.

To run this script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`.