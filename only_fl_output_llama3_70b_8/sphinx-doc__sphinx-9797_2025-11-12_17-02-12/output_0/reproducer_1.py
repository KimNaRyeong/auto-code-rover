import os
import sys
from sphinx.cmd.build import build_main
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

# Create a temporary directory for the documentation
tmp_dir = 'tmp_doc'
os.makedirs(tmp_dir, exist_ok=True)

# Create the Python module with the classes
module_file = os.path.join(tmp_dir, 'spam.py')
with open(module_file, 'w') as f:
    f.write('''
class Parent:
    @classmethod
    def method(cls) -> int:
        """Return an integer."""
        return 17

class Child(Parent):
    @classmethod
    def method(cls):
        return 42
''')

# Create the Sphinx configuration file
conf_file = os.path.join(tmp_dir, 'conf.py')
with open(conf_file, 'w') as f:
    f.write('''
project = "spam"
extensions = ["sphinx.ext.autodoc"]
''')

# Create the documentation index file
index_file = os.path.join(tmp_dir, 'index.rst')
with open(index_file, 'w') as f:
    f.write('''
spam
====

.. automodule:: spam
   :members:
   :undoc-members:
''')

# Build the documentation
sys.argv = ['', '-b', 'html', tmp_dir, os.path.join(tmp_dir, '_build')]
try:
    build_main()
except SystemExit as e:
    if e.code != 0:
        raise

# Check if the docstring is inherited
with open(os.path.join(tmp_dir, '_build', 'html', 'spam.html'), 'r') as f:
    html = f.read()
    assert "Return an integer." in html
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present, exiting with code 0")
exit(0)
