from docutils.parsers.rst import directives
from docutils.core import publish_string
import html

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
    rst_string = """
.. role:: kbd
:kbd:`Control-x Control-f`
"""
    html_string = publish_string(rst_string, writer_name='html').decode('utf-8')

    assert '<kbd>Control</kbd>-<kbd>x</kbd> <kbd>Control</kbd>-<kbd>f</kbd>' in html_string
    if '<kbd>Control-x Control-f</kbd>' in html_string:
        raise AssertionError("Expected nested or individual <kbd> elements but got a single <kbd> element")

if __name__ == '__main__':
    try:
        test_kbd_role()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
