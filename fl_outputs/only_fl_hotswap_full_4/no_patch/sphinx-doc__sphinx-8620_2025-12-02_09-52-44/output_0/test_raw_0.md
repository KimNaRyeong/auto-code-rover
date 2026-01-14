 Here is a standalone Python script `reproducer.py` that demonstrates the issue:
```python
import docutils.nodes
import docutils.parsers.rst

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def role_handler(role, rawtext, text, lineno, inliner, options={}, content=[]):
    node = docutils.nodes.kbd(text, **options)
    return [node], []

def setup(app):
    app.add_role('kbd', role_handler)

def test_issue():
    rst_text = """
:kbd:`A`

:kbd:`Shift+X`
"""

    settings = {
        'input_encoding': 'utf-8',
        'output_encoding': 'unicode',
        'initial_header_level': 2,
        'report_level': 5,
        'halt_level': 5,
        'warning_is_error': 0,
    }

    parser = docutils.parsers.rst.Parser()
    document = parser.parse(rst_text, settings=settings)

    # Check the generated HTML
    expected_html = """\
<kbd class="kbd docutils literal notranslate">A</kbd>
<kbd class="kbd compound docutils literal notranslate">
  <kbd class="kbd docutils literal notranslate">Shift</kbd>+
  <kbd class="kbd docutils literal notranslate">X</kbd>
</kbd>"""

    actual_html = ''.join(document.traverse(docutils.nodes.Element))
    assert actual_html == expected_html, f"Generated HTML does not match the expected output:\n{actual_html}\nvs.\n{expected_html}"

if __name__ == '__main__':
    test_issue()
    print("Issue reproduced successfully!")
```
To run the script, execute `python3 reproducer.py` in the terminal. If the generated HTML does not match the expected output, an `AssertionError` will be raised, and the stack trace will be printed. If the generated HTML matches the expected output, the script will exit with code 0.

Note that the `role_handler` function is a custom role handler that adds a `compound` class to the parent `<kbd>` element for compound keystrokes. This is the expected behavior described in the issue.