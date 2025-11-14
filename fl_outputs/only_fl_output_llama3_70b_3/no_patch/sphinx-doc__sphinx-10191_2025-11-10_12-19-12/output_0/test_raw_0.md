Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder
from sphinx.writers.latex import LaTeXWriter

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
    src_dir = os.path.dirname(__file__)
    out_dir = os.path.join(src_dir, '_build', 'latex')
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'latex')
    app.builder = LaTeXBuilder(app)
    app.writer = LaTeXWriter(app)

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

    with open(os.path.join(out_dir, 'index.pdf'), 'rb') as f:
        pdf_content = f.read()

    if b'?' in pdf_content:
        raise AssertionError("Footnote mark is rendered as '?'")

if __name__ == '__main__':
    reproduce_issue()
```
<|start_header_id|>