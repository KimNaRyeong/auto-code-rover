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

def test_latex_output():
    srcdir = os.path.dirname(__file__)
    outdir = os.path.join(srcdir, 'outdir')
    app = Sphinx(srcdir, srcdir, outdir, outdir, 'latex', verbosity=0)
    app.add_role('python', 'code')
    app.builder = LaTeXBuilder(app)

    index_rst = '''
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
'''
    with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
        f.write(index_rst)

    app.build()

    latex_file = os.path.join(outdir, 'latex', 'index.tex')
    with open(latex_file) as f:
        latex_content = f.read()

    assert '\\sphinxcode{\\sphinxupquote{%\n' in latex_content, "No leading whitespace"
    assert '%}\n}\\end{sphinxcode}' in latex_content, "No trailing whitespace"

try:
    test_latex_output()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script creates a Sphinx project with a single `index.rst` file containing the example code block. It then builds the LaTeX output and checks if the generated `.tex` file contains leading and trailing whitespace characters around the inline code block. If the issue is present, it raises an `AssertionError`, prints the stack trace, and exits with code 1. If the issue is fixed, it exits with code 0.