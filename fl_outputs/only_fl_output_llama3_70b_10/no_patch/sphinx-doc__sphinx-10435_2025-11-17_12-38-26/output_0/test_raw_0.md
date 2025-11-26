Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
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
    srcdir = os.path.dirname(__file__)
    outdir = os.path.join(srcdir, '_build', 'latex')
    app = Sphinx(srcdir, srcdir, outdir, outdir, 'latex', False, [])
    app.add_role('python', 'code')

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

    app.builder = LaTeXBuilder(app)
    app.builder.build_all()

    latex_file = os.path.join(outdir, 'index.tex')
    with open(latex_file, 'r') as f:
        latex_content = f.read()

    expected_latex_content = r'''
\documentclass{manual}
\begin{document}

Inline \sphinxcode{\sphinxupquote{%%
\PYG{k}{def} \PYG{n+nf}{foo}\PYG{p}{(}\PYG{l+m+mi}{1} \PYG{o}{+} \PYG{l+m+mi}{2} \PYG{o}{+} \PYG{k+kc}{None} \PYG{o}{+} \PYG{l+s+s2}{\PYGZdq{}}\PYG{l+s+s2}{abc}\PYG{l+s+s2}{\PYGZdq{}}\PYG{p}{)}\PYG{p}{:} \PYG{k}{pass}%%
}} code block

\end{document}
'''

    if latex_content != expected_latex_content:
        raise AssertionError("Extra whitespace in LaTeX output")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a minimal Sphinx project, builds the LaTeX output, and checks if the generated LaTeX code contains extra whitespace at the start and end of the inline code block. If it does, an `AssertionError` is raised with a stack trace.