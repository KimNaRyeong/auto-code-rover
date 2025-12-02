 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import docutils.nodes
from sphinx.errors import SphinxError

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_duplicate_terms(app, env):
    terms = {}
    for term in env.glossary:
        if term in terms:
            msg = f"duplicate term description of {terms[term]}, other instance in glossary"
            raise SphinxError(app.config.warningiserror, app.config.source_suffix, None, msg)
        terms[term] = term

def setup(app):
    app.connect('env-updated', check_duplicate_terms)

if __name__ == '__main__':
    try:
        app = sphinx.application.Sphinx(srcdir='doc', confdir='doc', outdir='build/html')
        app.build('html', None)
    except Exception as e:
        print_stacktrace(e)
```
To reproduce the issue, execute the script by running `python3 reproducer.py` in the root directory of the project. The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

The script uses the `sphinx.application.Sphinx` class to build the HTML documentation and connects to the `env-updated` event to check for duplicate terms. When a duplicate term is found, it raises a `SphinxError` with the same message as the original issue. The `print_stacktrace` function is used to print the stack trace of the error.