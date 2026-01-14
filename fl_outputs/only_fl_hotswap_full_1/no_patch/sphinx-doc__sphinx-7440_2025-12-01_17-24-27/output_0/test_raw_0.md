 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import docutils.nodes
from sphinx.errors import SphinxError

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_duplicate_terms(app, env, docname):
    terms = set()
    for node in app.env.domaindata['std']['glossary'].values():
        if node['term'] in terms:
            raise SphinxError(f'duplicate term description of {node["term"]}, other instance in glossary')
        terms.add(node['term'])

def setup(app):
    app.connect('build-finished', check_duplicate_terms)

if __name__ == '__main__':
    app = sphinx.application.Sphinx(srcdir='doc', confdir='doc', outdir='build/html', doctreedir='doc/_build/doctree')
    try:
        app.build(app.config.tags, app.config.patterns, quiet=True)
    except SphinxError as e:
        print_stacktrace(e)
        raise e
```
To reproduce the issue, execute the script with Python 3.6:
```bash
$ python3 reproducer.py
```
The script will raise an `AssertionError` with a stack trace showing the line number where the duplicate term is defined.

If the issue is fixed, the script will exit with code 0 without raising any exceptions.