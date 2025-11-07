from docutils.core import publish_string
from docutils.nodes import document, paragraph, literal_block
from docutils.parsers.rst import roles
import os

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
    doc = publish_string(rst_string, writer_name='html')
    html_output = doc.decode('utf-8')
    try:
        assert '<kbd>Control</kbd>-<kbd>x</kbd>' in html_output or '<kbd>Control</kbd>-<kbd>f</kbd>' in html_output
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_kbd_role()
