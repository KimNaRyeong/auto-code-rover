Here is the reproducer script:

```python
import sphinx
from docutils.nodes import paragraph, text
from docutils.parsers.rst import Directive

def setup_sphinx():
    from docutils.core import publish_string
    from sphinx.application import SphinxApplication
    app = SphinxApplication()
    app.builder.build_doc('index', 'latex')
    return app.builder.get_text_output()

def test_issue():
    rst = r"""
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
"""
    app = setup_sphinx()
    output = publish_string(rst, writer_name='latex', settings_overrides={'latex_documents': [('index', 'index.tex', 'Document Title', 'Author Name', 'manual')]})
    if b'\\begin{code}' not in output:
        raise AssertionError("Expected whitespace at start and end of inline code")

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
```

This script sets up a Sphinx application, publishes the given RST content to LaTeX format, and checks if the expected whitespace is present. If not, it raises an `AssertionError` with a stack trace.