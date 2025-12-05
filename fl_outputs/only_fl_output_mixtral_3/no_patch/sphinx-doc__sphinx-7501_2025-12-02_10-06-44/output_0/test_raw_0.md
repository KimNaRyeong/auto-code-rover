 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import docutils
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

def setup():
    app = sphinx.application.Sphinx(srcdir='doc', confdir='doc', outdir='build/html')
    app.build(force_all=True)

if __name__ == '__main__':
    try:
        setup()
    except SphinxError as e:
