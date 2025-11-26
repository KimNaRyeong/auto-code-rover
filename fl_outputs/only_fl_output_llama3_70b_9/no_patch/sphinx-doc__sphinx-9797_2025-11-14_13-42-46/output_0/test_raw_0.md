Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import importlib.util
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutoDirective
from sphinx.builders.html import StandaloneHTMLBuilder

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

# Create a temporary directory for the documentation
doc_dir = "docs"
os.makedirs(doc_dir, exist_ok=True)

# Create a module with the classes
module_name = "spam"
module_file = f"{module_name}.py"
with open(module_file, "w") as f:
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
config_file = "conf.py"
with open(os.path.join(doc_dir, config_file), "w") as f:
    f.write("""
project = "spam"
extensions = ["sphinx.ext.autodoc"]
""")

# Create an index file for the documentation
index_file = os.path.join(doc_dir, "index.rst")
with open(index_file, "w") as f:
    f.write("""
spam
====

.. automodule:: spam
   :members:
   :undoc-members:
""")

# Build the documentation
builder = StandaloneHTMLBuilder(Sphinx(srcdir=doc_dir))
builder.build_all()

# Load the module and check if the documentation is inherited
spec = importlib.util.spec_from_file_location(module_name, module_file)
module = importlib.util.module_from_spec(spec)

try:
    assert module.Child.method.__doc__ == "Return an integer."
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present")
exit(0)
```
This script creates a temporary directory for the documentation, generates the necessary files (module, configuration file, and index file), builds the documentation using Sphinx, and then checks if the documentation is inherited correctly. If the issue is present, it raises an `AssertionError` with a stack trace; otherwise, it prints "Issue not present" and exits with code 0.