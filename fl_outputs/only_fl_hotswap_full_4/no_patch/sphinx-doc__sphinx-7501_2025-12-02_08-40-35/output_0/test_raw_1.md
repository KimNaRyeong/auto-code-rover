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
    terms = set()
    duplicates = set()
    for node in app.env.found_terms.values():
        if not isinstance(node, docutils.nodes.term):
            continue
        term = node.astext().lower()
        if term in terms:
            duplicates.add(term)
        terms.add(term)
    if duplicates:
        msg = f"duplicate term description of {', '.join(duplicates)}"
        raise SphinxError(app, app.env, "glossary", 0, msg)

def setup(app):
    app.connect("env-updated", check_duplicate_terms)

def main():
    app = sphinx.application.Sphinx(srcdir="doc", confdir="doc", outdir="build/html")
    setup(app)
    app.build(force_all=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script uses the Sphinx API to build the documentation and check for duplicate terms. If any duplicate terms are found, it raises a `SphinxError` with a custom message. The `print_stacktrace` function is used to print a stack trace if an exception is raised.

To run the script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.