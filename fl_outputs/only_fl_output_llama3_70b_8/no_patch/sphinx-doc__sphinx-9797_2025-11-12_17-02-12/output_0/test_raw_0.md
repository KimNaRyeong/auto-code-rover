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

app = Sphinx(srcdir='.', confdir='.')
app.add_directive('automodule', AutodocDirective)
app.add_domain(None)

try:
    docstring = inspect.getdoc(Child.method)
    assert docstring == "Return an integer."
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present, exiting with code 0")
exit(0)
```
This script defines the `Parent` and `Child` classes with the overridden class method. It then creates a Sphinx application and adds the `automodule` directive to it.

The script then tries to get the docstring of the `method` class method in the `Child` class using `inspect.getdoc`. If the docstring is not inherited from the parent class, an `AssertionError` is raised. The `print_stacktrace` function is used to print a detailed stack trace of the error.

If the issue is not present, the script prints a success message and exits with code 0.