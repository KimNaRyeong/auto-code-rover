Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import inspect
import os
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

# Create a temporary directory for the Sphinx build
tmp_dir = "tmp_sphinx_build"
os.makedirs(tmp_dir, exist_ok=True)

# Define the classes with overridden classmethod
class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42

# Create a Sphinx application and add the autodoc extension
app = Sphinx(tmp_dir, "src", tmp_dir, tmp_dir)
app.add_directive("automodule", AutodocDirective)

# Generate the documentation for the Child class
doc_output = app.builder.render("spam.Child", [".. autoclass:: spam.Child\n"])

# Check if the overridden classmethod inherits the documentation from the parent class
if "Return an integer." not in doc_output:
    raise AssertionError("Overridden classmethod does not inherit documentation from parent class")

print("Issue is fixed, exiting with code 0")
os._exit(0)
```
This script creates a temporary directory for the Sphinx build, defines the classes with overridden classmethod, generates the documentation using Sphinx and autodoc extension, and checks if the overridden classmethod inherits the documentation from the parent class. If not, it raises an `AssertionError` with a stack trace of the issue.