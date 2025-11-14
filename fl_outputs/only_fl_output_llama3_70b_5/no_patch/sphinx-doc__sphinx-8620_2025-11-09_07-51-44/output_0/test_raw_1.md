Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sys
from docutils.core import publish_string
from docutils.parsers.rst import directives, roles

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
    overrides = {'report_level': 5, 'halt_level': 5}
    pub = publish_string(rst, writer_name='html', settings_overrides=overrides)
    html = pub.parts['body']
    
    # Check if the issue is present
    assert '<kbd class="kbd compound">' not in html, "Expected no 'compound' class on container kbd element"
    try:
        assert '<kbd class="kbd">' in html, "Expected 'kbd' class on child kbd elements"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_kbd_role()
```
This script uses the `docutils` library to parse the RST input and generate HTML output. It then checks if the issue is present by verifying that the container `<kbd>` element does not have a CSS class `compound`, and the child `<kbd>` elements do have a CSS class `kbd`. If the issue is present, it raises an `AssertionError` with a stack trace.

Please make sure to install the required packages, including `docutils`, before running this script.