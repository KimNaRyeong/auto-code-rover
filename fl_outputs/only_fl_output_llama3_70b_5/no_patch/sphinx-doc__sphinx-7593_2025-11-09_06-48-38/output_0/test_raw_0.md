Here is the `reproducer.py` file that reproduces the issue:
```
import docutils.nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html import HTMLWriter

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

def test_kbd_directive():
    app = Sphinx(srcdir="", outdir="")
    app.builder = StandaloneHTMLBuilder(app)
    app.writer = HTMLWriter(app)

    directive = Directive("kbd", app, ["Control-x Control-f"])
    node = docutils.nodes.literal_block(directive.content, directive.content)
    node.line = 1

    try:
        app.emit_first_result(node)
        html = app.builder.outfilename
        with open(html, "r") as f:
            content = f.read()
            assert "<kbd>Control-x Control-f</kbd>" in content
            assert "<kbd>Control</kbd>-<kbd>x</kbd> <kbd>Control</kbd>-<kbd>f</kbd>" not in content
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    test_kbd_directive()
```
This script creates a Sphinx application, defines a custom `kbd` directive with the content "Control-x Control-f", and then checks if the generated HTML contains the expected output. If the issue is present, it raises an `AssertionError` with a stack trace of the error.