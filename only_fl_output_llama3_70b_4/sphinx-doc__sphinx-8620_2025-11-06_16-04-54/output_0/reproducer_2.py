import docutils.core
from docutils.writers import html4css1
from docutils.parsers.rst import directives

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

def reproduce_issue():
    rst_text = """
:kbd:`A`

:kbd:`Shift+X`
"""
    document = docutils.core.publish_string(rst_text, writer=html4css1.Writer())
    html_output = document.decode('utf-8')

    assert '<kbd class="compound">' in html_output, "Compound kbd element is not marked with a CSS class"
    print("Issue fixed. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
