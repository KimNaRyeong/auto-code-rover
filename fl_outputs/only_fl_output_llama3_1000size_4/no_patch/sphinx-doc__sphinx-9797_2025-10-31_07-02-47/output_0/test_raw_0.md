Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.application import SphinxApplication
import inspect
import sys
import traceback

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
    try:
        Parent = type("Parent", (), {"method": staticmethod(Parent.method)})
        Child = type("Child", (Parent,), {"method": Child.method})
        
        sphinx_app = SphinxApplication()
        sphinx_app.builder = autodoc.AutoDocumentBuilder(sphinx_app, outdir="docs")
        sphinx_app.config.autodoc_member_order = 'bysource'
        
        sphinx_app.build_all()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a Parent and Child class with the same structure as in your issue, then attempts to build Sphinx documentation for these classes. If the issue is present (i.e., the overridden classmethod does not inherit the documentation from the parent class), it prints the stack trace of the exception and raises an `AssertionError`.