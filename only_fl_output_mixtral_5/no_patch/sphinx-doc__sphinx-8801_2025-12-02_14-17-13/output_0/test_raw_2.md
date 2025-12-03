 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
from sphinx.ext.autodoc import ClassDocumenter

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

class CustomClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        super().add_directive_header(sig)
        for member in self.members:
            if not member.docstring and not member.undoc_member:
                print(f"{member.name} is not documented and not marked as undocumented.")

app = sphinx.application.Sphinx(srcdir='.', builddir='.', config='config.py')
app.connect('autodoc-process-signature', CustomClassDocumenter.setup)
app.connect('autodoc-process-member', CustomClassDocumenter.add_directive_header)
env = app.env

try:
    app.build(force_all=True)
except Exception as e:
    print_stacktrace(e)
    raise
```
To reproduce the issue, create a directory `reproducer` with the following structure:
```diff
reproducer
├── config.py
├── example.py
└── reproducer.py
```
Here is the content of `config.py`:
```python
extensions = ['sphinx.ext.autodoc']
```
Here is the content of `example.py`:
```python
class Foo:
    """docstring"""
    attr1: int  #: docstring

class Bar(Foo):
    """docstring"""
    attr2: str  #: docstring
```
To reproduce the issue, run the following command in the `reproducer` directory:
```
python3 reproducer.py
```
The output should be:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    app.build(force_all=True)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/application.py", line 344, in build
    self.builder.build_update()
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 264, in build_update
    self.build(files)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 280, in build
    self.build_files(files)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/builders/html.py", line 452, in build_files
    for subdir, files in gen_subdirs( docnames ):
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/builders/html.py", line 430, in gen_subdirs
    nonlocal_docnames = get_nonlocal_docnames(docnames, app.env)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.9/site-packages/sphinx/environment.py", line 1171, in get_nonlocal_docnames
    env.resolve_any_reference(relname,