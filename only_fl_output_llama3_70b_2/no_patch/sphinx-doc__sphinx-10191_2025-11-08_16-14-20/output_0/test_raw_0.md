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
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'latex', False, [])
    app.builder = LaTeXBuilder(app)
    app.writer = LaTeXWriter(app)

    index_rst = """
Test
=====

Explicitly numbered footnotes
---------------------------

First reference to first footnote [1]_

First reference to second footnote [2]

Second reference to first footnote [1]

Second reference to second footnote [2]_


.. rubric:: Footnotes

.. [1] A first footnote

.. [2] A second footnote
"""

    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write(index_rst)

    app.build()

    with open(os.path.join(out_dir, 'test.pdf'), 'rb') as f:
        pdf_content = f.read().decode('latin-1')

    if '?' in pdf_content:
        raise AssertionError("Footnote mark is rendered as '?'")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
```
This script creates a Sphinx project with the given `index.rst` file, builds it to LaTeX and PDF, and checks if the resulting PDF contains a `?` character. If it does, it raises an `AssertionError`.