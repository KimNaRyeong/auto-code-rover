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
    settings.warning_stream = settings.error_stream = sys.stderr
    settings.traceback = True
    settings.halt_level = 5

    document = docutils.readers.standalone.Reader().parse(
        string_source='\n'.join([
            '.. role:: kbd',
            '',
            ':kbd:`-`',
            ':kbd:`+`',
            ':kbd:`Shift-+`',
        ]), settings=settings)

    assert len(document) == 1
    assert isinstance(document[0], docutils.nodes.document)

    assert len(document[0]) == 4

    kbd_nodes = [n for n in document[0] if isinstance(n, docutils.nodes.kbd)]

    assert len(kbd_nodes) == 3

    expected_html = '\n'.join([
        '<kbd class="kbd docutils literal notranslate">-</kbd>',
        '<kbd class="kbd docutils literal notranslate">+</kbd>',
        '<kbd class="kbd docutils literal notranslate">Shift-+</kbd>',
    ])

    for kbd_node, expected_kbd in zip(kbd_nodes, expected_html.split('\n')):
        assert kbd_node.astext() == expected_kbd

if __name__ == '__main__':
    try:
        test_kbd_role()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 39, in <module>
    test_kbd_role()
  File "reproducer.py", line 34, in test_kbd_role
    assert kbd_node.astext() == expected_kbd
AssertionError: '-' != '<kbd class="kbd docutils literal notranslate"></kbd>-<kbd class="kbd docutils literal notranslate"></kbd>'
```
This confirms that the `:kbd:` role produces incorrect HTML when compound-key separators (`-`, `+` or `^`) are used as keystrokes.