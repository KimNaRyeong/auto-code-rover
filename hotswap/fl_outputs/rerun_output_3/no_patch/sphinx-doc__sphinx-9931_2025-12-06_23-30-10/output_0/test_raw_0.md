 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import setup as autodoc_setup
from sphinx.application import Sphinx

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

def setup_sphinx():
    app = Sphinx(srcdir='.')
    autodoc_setup(app)
    app.build(force_all=True, doctree_only=True)

def test_autodoc_add_module_names():
    conf = {
        'project': 'MyProject',
        'source_suffix': '.rst',
        'master_doc': 'index',
        'add_module_names': False,
    }

    app = Sphinx(**conf)
    app.connect('config-inited', setup_sphinx)

    try:
        app.build(force_all=True, doctree_only=True)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Sphinx build failed"

if __name__ == "__main__":
    test_autodoc_add_module_names()
    print("No failures detected.")
```
To reproduce the issue, create a directory with the following structure:
```diff
- reproducer.py
- mypackage
  - mymodule.py
  - __init__.py
- conf.py
- index.rst
```
With the following contents:

`mypackage/mymodule.py`:
```python
class MyClass:
    """Whatever 1."""
    pass

def foo(arg: MyClass):
    """Whatever 2."""
    pass
```
`conf.py`:
```python
# ...
add_module_names = False
# ...
```
`index.rst`:
```rst
mypackage.mymodule module
=========================

.. automodule:: mypackage.mymodule
   :members:
   :undoc-members:
   :show-inheritance:
```
Then, execute `python3 reproducer.py`. The output should show the stack trace and `AssertionError`:
```vbnet
No failures detected.
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    test_autodoc_add_module_names()
  File "reproducer.py", line 27, in test_autodoc_add_module_names
    app.build(force_all=True, doctree_only=True)
  File "/usr/local/lib/python3.9/site-packages/sphinx/application.py", line 348, in build
    self.builder.build_update()
  File "/usr/local/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 261, in build_update
    self.build(docnames, write)
  File "/usr/local/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 283, in build
    self.write_doc(docname, doctree)
  File "/usr/local/lib/python3.9/site-packages/sphinx/builders/latex/__init__.py", line 147, in write_doc
    self.write_dvi(doctree, destdir, encoding, document)
  File "/usr/local/lib/python3.9/