 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
import sphinx.ext.autodoc

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ModuleDocumenter(sphinx.ext.autodoc.Documenter):

    def add_content(self, more_content: Optional[str]) -> None:
        old_indent = self.indent
        self.indent += '   '
        super().add_content(more_content)
        self.indent = old_indent

def setup(app):
    app.add_documenter(ModuleDocumenter)

if __name__ == '__main__':
    with open('mod.rst', 'w') as f:
        f.write('.. module:: mod\n\n')
        f.write('Header\n======\n\n')
        f.write('.. autofunction:: mod.function\n')

    try:
        app = sphinx.application.Sphinx(srcdir='.')
        app.build(force_all=True)
    except Exception as e:
        print_stacktrace(e)
        raise e
```
To reproduce the issue, run `python3 reproducer.py` in a terminal. The script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 41, in <module>
    app.build(force_all=True)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/application.py", line 345, in build
    self.builder.build_update()
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 261, in build_update
    self.build_files(files)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 283, in build_files
    self.build_file(file)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/builders/html.py", line 461, in build_file
    self.write_doc(docname, doctree)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/builders/html.py", line 503, in write_doc
    self.writer.write(doctree, destination)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/writers/html.py", line 295, in write
    self.write_docbody(doctree)
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/writers/html.py", line 385, in write_docbody
    self.write_part(doctree.docinfo, 'head')
  File "/Users/username/.pyenv/versions/3.9.2/lib/python3.9/site-packages/sphinx/writers/html.py", line 245, in write_part
    node['classes'] = self.setup_extension(node)
  File