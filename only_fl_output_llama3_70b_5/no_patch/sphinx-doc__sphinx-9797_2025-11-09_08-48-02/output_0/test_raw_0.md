Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective
from docutils.parsers.rst import directives

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

# Define the module with the overridden classmethod
module_code = """
class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42
"""

with open("src/spam.py", "w") as f:
    f.write(module_code)

# Configure Sphinx
config = """
[autodoc]
imported_members = True

[html]
theme = alabaster
"""

with open("docs/conf.py", "w") as f:
    f.write(config)

index_rst = """
spam
====

.. automodule:: spam
   :members:
   :undoc-members:
"""

with open("docs/index.rst", "w") as f:
    f.write(index_rst)

# Build Sphinx documentation
sys.path.insert(0, "src")
app = Sphinx("docs", "build", "tmp_sphinx_build", "docs/conf.py")
app.build()

# Check if the overridden classmethod has inherited the documentation
with open(os.path.join(tmp_dir, "spam.html")) as f:
    html_content = f.read()
    assert "Return an integer" in html_content, "Overridden classmethod did not inherit documentation"

print("Issue is fixed!")
sys.exit(0)
```
This script creates a temporary directory for the Sphinx build, defines the module with the overridden classmethod, configures Sphinx, builds the documentation, and checks if the overridden classmethod has inherited the documentation. If the issue is present, it raises an `AssertionError` with a stack trace of the issue.