 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import TemplateBridge
from sphinx.writers.html import HTMLWriter
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.nodes import nested_parse_with_titles

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    app = sphinx.application.Sphinx(source_dir='.', builder=StandaloneHTMLBuilder(standalone_mode=False))
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', lambda app, what, name, obj, options, lines: lines)
    app.connect('builder-inited', lambda app: app.builder.add_transform(TemplateBridge()))

    env = app.env
    settings = app.config

    # Parse the reST document
    with open('index.rst') as f:
        docnode = nested_parse_with_titles(f.read(), env)

    # Render the document to HTML
    html_writer = HTMLWriter(env, None)
    html_writer.translator.body_pre_doc(docnode)
    html_writer.translator.visit_document(docnode)
    for node in docnode:
        html_writer.translator.visit_target(node)
        html_writer.translator.visit_rubric(node)
        html_writer.translator.depart_rubric(node)
        html_writer.translator.depart_target(node)
    html_writer.translator.depart_document(docnode)

    # Check if the reference text is broken
    reference_node = docnode[0].traverse(lambda node: node.get('names', []) == ['reference'])
    assert reference_node is not None, "Reference node not found"
    reference_text = reference_node.astext()
    assert reference_text == "This rubric will be a `broken` reference", "Reference text is broken"

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, create a directory `sphinx-rubric-issue` and put the `reproducer.py` script in it. Then, create a file `index.rst` in the same directory with the following content:
```rst
.. _reference:

.. rubric:: This rubric will be a ``broken`` reference

Let's call the :ref:`reference`
```
Finally, run the script with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised with a stack trace. If the issue is fixed, the script will exit with code 0.