Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sphinx
from sphinx.ext import autodoc
from sphinx.application import SphinxApplication

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
        sphinx.application.SphinxApplication(
            src_dir='src',
            conf_dir='docs',
            builder_name='html'
        )
        autodoc.autodoc(Child.method, docstring=True)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to build the Sphinx documentation for the given classes. If the issue is present, it will print a stack trace and raise an `AssertionError`.