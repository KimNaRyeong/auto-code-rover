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

def test_latex_output():
    srcdir = os.path.dirname(__file__)
    outdir = os.path.join(srcdir, 'outdir')
    app = Sphinx(srcdir, srcdir, outdir, outdir, 'latex', verbosity=0)
    app.add_role('python', 'code')
    app.builder = LaTeXBuilder(app)

    docname = 'index'
    doctree = app.env.get_doctree(docname)
    writer = LaTeXWriter(doctree)

    with open(os.path.join(outdir, f'{docname}.tex'), 'w') as f:
        writer.write(f, doctree)

    with open(os.path.join(outdir, f'{docname}.tex'), 'r') as f:
        latex_code = f.read()

    expected_latex_code = r'\sphinxcode{\sphinxupquote{%\PYG{k}{def} \PYG{n+nf}{foo}\PYG{p}{(}\PYG{l+m+mi}{1} \PYG{o}{+} \PYG{l+m+mi}{2} \PYG{o}{+} \PYG{k+kc}{None} \PYG{o}{+} \PYG{l+s+s2}{\PYGZdq{}}\PYG{l+s+s2}{abc}\PYG{l+s+s2}{\PYGZdq{}}\PYG{p}{)}\PYG{p}{:} \PYG{k}{pass}%}}'
    if latex_code.find(expected_latex_code) == -1:
        raise AssertionError("Extra whitespace found in LaTeX output")

if __name__ == '__main__':
    try:
        test_latex_output()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a Sphinx application, adds the `python` role, and builds the LaTeX output. It then checks if the generated LaTeX code contains extra whitespace at the start and end of the inline code block. If it does, an `AssertionError` is raised with a stack trace.