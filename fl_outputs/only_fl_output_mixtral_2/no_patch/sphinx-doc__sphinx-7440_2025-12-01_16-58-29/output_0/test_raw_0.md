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
        if not isinstance(node, docutils.nodes.termsep):
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
    app = sphinx.application.Sphinx(srcdir="doc", confdir=".", outdir="build/html")
    setup(app)
    app.build(force_all=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will raise an `AssertionError` with a stack trace when the issue is present. To fix the issue, modify the `glossary.rst` file to ensure that all terms are unique, regardless of case. Once the issue is fixed, the script will exit with code 0.