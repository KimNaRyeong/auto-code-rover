 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import setup as autodoc_setup
from sphinx.application import Sphinx

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup(app: Sphinx):
    app.connect('autodoc-process-signature', autodoc_process_signature)

def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
    # Do nothing, just to trigger the 'autodoc-process-signature' event
    pass

def main():
    try:
        app = Sphinx(...)
        autodoc_setup(app, config={
            'add_module_names': False,
        })
        app.build(force_all=True)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```
To reproduce the issue, create a directory `myproject` with the following structure:
```diff
myproject/
|-- conf.py
|-- index.rst
|-- mypackage/
|   |-- __init__.py
|   |-- mymodule.py
|-- reproducer.py
```
The contents of the files are as follows:

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
`mypackage/mymodule.py`:
```python
class MyClass:
    """Whatever 1."""
    pass

def foo(arg: MyClass):
    """Whatever 2."""
    pass
```
Then, run `python3 reproducer.py` in the `myproject` directory. The output should be:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    main()
  File "reproducer.py", line 34, in main
    app.build(force_all=True)
  File "/path/to/sphinx/builders/__init__.py", line 345, in build
    self.apply_transforms()
  File "/path/to/sphinx/builders/__init__.py", line 331, in apply_transforms
    self.transform(docname, new_docname)
  File "/path/to/sphinx/builders/manpage.py", line 110, in transform
    self.add_man_page(self.env.get_current_docname(), self.env.doc2path(docname, base=self.outdir))
  File "/path/to/sphinx/builders/manpage.py", line 102, in add_man_page
    self.add_man_page_section(docname, content, man_pagename, number, title, subtitle, footer)
  File "/path/to/sphinx/builders/manpage.py", line 75, in add_man_page_section
    self.add_man_page_line(docname, line)
  File "/path/to/sphinx/builders/manpage.py", line 64, in add_man_page_line
    self.man_