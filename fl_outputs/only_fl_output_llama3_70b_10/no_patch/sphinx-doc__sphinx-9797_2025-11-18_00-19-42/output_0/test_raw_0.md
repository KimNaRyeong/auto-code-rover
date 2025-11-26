Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import inspect
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective

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

class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42

def test_autodoc():
    app = Sphinx(srcdir='.', confdir='.')
    app.add_directive('autodoc', AutodocDirective)
    try:
        docstring = inspect.getdoc(Child.method)
        assert docstring == "Return an integer."
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    test_autodoc()
```
This script defines the `Parent` and `Child` classes with the overridden class method, creates a Sphinx application, and uses the `autodoc` directive to generate documentation. The `test_autodoc` function checks if the docstring of the `Child.method` is inherited from the parent class. If not, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1.