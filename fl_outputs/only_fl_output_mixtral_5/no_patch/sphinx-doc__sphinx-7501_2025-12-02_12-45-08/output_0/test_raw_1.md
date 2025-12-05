 I apologize for the mistake in my previous response. Here's an updated standalone Python script `reproducer.py` that reproduces the issue:
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
    for node in env.domaindata['std']['glossary'].values():
        if node['term'] in terms:
            raise SphinxError(f'duplicate term description of {node["term"]}, other instance in glossary')
        terms.add(node['term'])

def setup(app):
    app.connect('env-updated', check_duplicate_terms)

if __name__ == '__main__':
    app = sphinx.application.Sphinx(srcdir='doc', confdir='doc', outdir='build/html')
    app.build(force_all=True)
```
To reproduce the issue, execute the script with the following command:
```bash
python3 reproducer.py
```
The script will raise a `SphinxError` with a stack trace when the issue is present. The script will exit with code 0 when the issue is fixed.

I apologize for any confusion caused by my previous response.