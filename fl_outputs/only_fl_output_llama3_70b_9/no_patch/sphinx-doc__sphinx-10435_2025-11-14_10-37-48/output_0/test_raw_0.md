Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
from sphinx.application import Sphinx
from sphinx.builders.latex import LaTeXBuilder

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
    srcdir = os.path.dirname(__file__)
    outdir = os.path.join(srcdir, '_build', 'latex')
    app = Sphinx(srcdir, srcdir, outdir, outdir, 'latex')
    app.builder = LaTeXBuilder(app)
    
    try:
        with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
            f.write("""
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
""")
        app.build()
        
        with open(os.path.join(outdir, 'index.tex'), 'r') as f:
            tex_content = f.read()
            assert '\sphinxcode{\sphinxupquote{%' not in tex_content, "Whitespace at start and end of inline code"
            assert '%}\sphinxcode{' not in tex_content, "Whitespace at start and end of inline code"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    reproduce_issue()
```
This script creates a minimal Sphinx project with an `index.rst` file containing the problematic inline code block. It then builds the LaTeX output and checks if the generated `index.tex` file contains whitespace at the start and end of the inline code block. If it does, it raises an `AssertionError` with a stack trace.