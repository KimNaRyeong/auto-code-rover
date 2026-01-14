 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx.ext.autodoc as autodoc

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup():
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='_build/html')
    app.add_extension('sphinx.ext.autodoc')
    app.connect('config-inited', autodoc.setup)
    try:
        app.build(force_all=True, warningiserror=True)
    except Exception as e:
        print_stacktrace(e)
        app.exit(1)

if __name__ == '__main__':
    setup()
```
To reproduce the issue, create a file `index.rst` in the same directory as `reproducer.py` with the following content:
```rst
============
Reproduce
============

.. c:function:: int foo(int bar)

   :param int bar: Bar
```
Then run the script with `python3 reproducer.py`. The output should be similar to the one in the issue description:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    setup()
  File "reproducer.py", line 17, in setup
    app.build(force_all=True, warningiserror=True)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/application.py", line 349, in build
    self.builder.build_update()
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/html.py", line 284, in build_update
    self.build_files(files)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/html.py", line 308, in build_files
    for fn in genfiles:
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/__init__.py", line 293, in _write_serial
    self.write(write, docname, doctree)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/html.py", line 454, in write
    self.writer.write(doctree, builder, 'html', doctree.docname)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 20, in write
    self.write_doctree(doctree, builder)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 46, in write_doctree
    self.document(doctree, builder)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 128, in document
    self.translator.visit_document(doctree)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 234, in visit_document
    self.head_prefix += self.get_settings(
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/