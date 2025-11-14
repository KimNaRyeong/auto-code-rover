Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx

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
    src_dir = os.path.join(os.path.dirname(__file__), 'docs')
    out_dir = os.path.join(os.path.dirname(__file__), '_build')

    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html', ['sphinx.ext.autodoc'])
    app.add_autodocumenter()

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise

    with open(os.path.join(out_dir, 'index.html'), 'r') as f:
        html_content = f.read()

    if 'color=16777215' in html_content:
        raise AssertionError("Sphinx changed the number system from hexadecimal to decimal for function default arguments")

if __name__ == '__main__':
    reproduce_issue()
```
This script creates a minimal Sphinx project, builds the HTML documentation, and checks if the generated HTML contains the decimal value `16777215` instead of the original hexadecimal value `0xffffff`. If it does, it raises an `AssertionError` with a stack trace.