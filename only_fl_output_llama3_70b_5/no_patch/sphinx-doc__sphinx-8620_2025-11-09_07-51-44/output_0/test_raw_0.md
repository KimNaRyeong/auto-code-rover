Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import docutils.nodes
from docutils.parsers.rst import directives, roles
from docutils.core import publish_string

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

def test_kbd_role():
    rst = """
:kbd:`A`

:kbd:`Shift+X`
"""
    document = docutils.nodes.document()
    directives.register_directive('kbd', roles.KBDRole)
    publish_string(rst, document=document)

    # Check if the issue is present
    kbd_elements = document.findall(condition=lambda node: isinstance(node, docutils.nodes.literal_block) and 'kbd' in node['classes'])
    assert len(kbd_elements) == 2, "Expected 2 kbd elements"
    single_keystroke_kbd = kbd_elements[0]
    compound_keystroke_kbd = kbd_elements[1]

    # Check if the container kbd element has a CSS class
    try:
        assert 'compound' in compound_keystroke_kbd['classes'], "Expected 'compound' class on container kbd element"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_kbd_role()
```
This script uses the `docutils` library to parse the RST input and generate HTML output. It then checks if the issue is present by verifying that the container `<kbd>` element has a CSS class `compound`. If the issue is present, it raises an `AssertionError` with a stack trace.