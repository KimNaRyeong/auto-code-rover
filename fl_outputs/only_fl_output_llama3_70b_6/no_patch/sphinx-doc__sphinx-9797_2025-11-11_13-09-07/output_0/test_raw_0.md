Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import importlib.util
import inspect
import os
import sphinx.application
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

# Create a module with the classes
module_path = os.path.join(tmp_dir, "spam.py")
with open(module_path, "w") as f:
    f.write("""
class Parent:
    @classmethod
    def method(cls) -> int:
        \"\"\"Return an integer.\"\"\"
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42
""")

# Create a Sphinx configuration file
conf_path = os.path.join(tmp_dir, "docs", "conf.py")
os.makedirs(os.path.dirname(conf_path), exist_ok=True)
with open(conf_path, "w") as f:
    f.write("""
project = "spam"
extensions = ["sphinx.ext.autodoc"]
""")

# Create a Sphinx documentation index file
index_path = os.path.join(tmp_dir, "docs", "index.rst")
os.makedirs(os.path.dirname(index_path), exist_ok=True)
with open(index_path, "w") as f:
    f.write("""
spam
====

.. automodule:: spam
   :members:
   :undoc-members:
""")

# Build the Sphinx documentation
app = sphinx.application.Sphinx(srcdir=tmp_dir, confdir=tmp_dir, outdir=os.path.join(tmp_dir, "_build"))
app.build()

# Load the module and inspect the documentation
spec = importlib.util.spec_from_file_location("spam", module_path)
module = importlib.util.module_from_spec(spec)

parent_doc = inspect.getdoc(module.Parent.method)
child_doc = inspect.getdoc(module.Child.method)

try:
    assert child_doc == parent_doc, "Overridden classmethod documentation not inherited"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script creates a temporary directory with the necessary files to reproduce the issue. It then builds the Sphinx documentation and inspects the documentation of the `Child` class method. If the documentation is not inherited from the parent class, it raises an `AssertionError` with a stack trace.