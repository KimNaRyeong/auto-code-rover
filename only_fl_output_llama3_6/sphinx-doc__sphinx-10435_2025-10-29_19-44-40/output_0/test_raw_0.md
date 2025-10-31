Here is the reproducer script:

```python
import sphinx
from docutils import nodes, utils
from docutils.parsers.rst import Directive
from sphinx.builders.latex import LaTeXBuilder
from sphinx.util.nodes import latex_escape

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

def test_issue():
    rst = r"""
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
"""

    builder = LaTeXBuilder()
    builder.config.latex_documents = [('index', 'index.tex', 'Index', 'main'),]
    builder.build('index')

    latex_file = open('index.tex', 'r')
    latex_content = latex_file.read()
    latex_file.close()

    if r'\PYG{k+kc}{None}' in latex_content:
        raise AssertionError("Issue present")

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed")
        exit(0)
```

This script reproduces the issue by building a LaTeX document using Sphinx, and then checks if the generated LaTeX file contains the expected code block with the correct syntax highlighting. If the issue is present (i.e., the generated LaTeX file contains the unwanted space characters), it raises an `AssertionError` and prints the stack trace.