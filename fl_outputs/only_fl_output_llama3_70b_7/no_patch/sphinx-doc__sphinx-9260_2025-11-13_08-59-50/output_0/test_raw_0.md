Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.application import Sphinx
from sphinx.util.console import bold, darkgreen

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

def test_linkchecker():
    src_dir = 'src'
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write("""
.. _make-changes:

Make Changes
==========

This is a sample page.

""")

    app = Sphinx(src_dir, src_dir, 'build', 'html')
    app.builder = StandaloneHTMLBuilder(app)
    try:
        app.build()
        html_file = os.path.join('build', 'index.html')
        with open(html_file, 'r') as f:
            html_content = f.read()
        assert '<a name="make-changes"></a>' in html_content
        assert '<a id="user-content-make-changes" class="anchor" aria-hidden="true" href="#make-changes">' in html_content
        linkchecker_output = app.builder.linkchecker.check(html_file)
        for error in linkchecker_output:
            if 'https://github.com/crate/crate-docs-theme/blob/master/DEVELOP.rst#make-changes' in str(error):
                raise AssertionError("Linkchecker croaks on anchor #make-changes")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_linkchecker()
```
This script creates a minimal Sphinx project with an `index.rst` file containing an anchor, builds the HTML documentation, and then checks the link using the `linkchecker`. If the linkchecker raises an error on the anchor `#make-changes`, it will raise an `AssertionError` with a stack trace.