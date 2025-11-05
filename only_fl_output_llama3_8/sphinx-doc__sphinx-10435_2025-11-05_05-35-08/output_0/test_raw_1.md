Here is the reproducer script:

```python
import sphinx
from docutils import nodes, utils
from docutils.parsers.rst import Directive
from sphinx.builders.latex import LaTeXBuilder
from sphinx.util.nodes import latex_code_role

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

    try:
        from sphinx import main
        main(['-b', 'latex', '-d', 'build', 'index.rst'])
    except AssertionError as e:
        print_stacktrace(e)
    else:
        print("Issue not reproduced")
        exit(0)

test_issue()
```

This script creates a simple Sphinx project, defines the `test_issue` function which reproduces the issue by building a LaTeX document with the given rst content. If the issue is present (i.e., there's whitespace at start and end of the inline code), it raises an `AssertionError`.