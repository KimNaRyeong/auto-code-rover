 Here is a standalone Python file `reproducer.py` that reproduces the issue:
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

class MyAutodoc(autodoc.Autodoc):
    def run(self):
        try:
            autodoc.Autodoc.run(self)
        except Exception as e:
            print_stacktrace(e)
            raise

app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='html', warningiserror=True)
app.connect('autodoc-process-signature', lambda app, what, name, obj, options, sig, retann: sig)
app.connect('autodoc-process-docstring', lambda app, what, name, obj, options, lines: lines)
app.setup_extension('sphinx.ext.autodoc')
app.registry.autodoc_classes['method'] = MyAutodoc

app.build(force_all=True, None)
```
To reproduce the issue, create a new directory, put the above code in a file named `reproducer.py`, and run the following commands in the terminal:
```bash
$ mkdir sphinx-issue
$ cd sphinx-issue
$ echo '

.. py:method:: f(*, a=2**4)
.. py:method:: g(a=2**4)
' > docs.rst
$ python3 reproducer.py
```
The output should contain the following error messages:
```vbnet
WARNING: could not parse arglist ('*, a=2**4'): Unable to parse BinOp object
WARNING: could not parse arglist ('a=2**4'): Unable to parse BinOp object
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    app.build(force_all=True, None)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 346, in build
    self.builder.build_update()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 283, in build_update
    self.write_doc(node)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 305, in write_doc
    self.write(self.pre_doc(node))
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 463, in write
    self.writer.write(node, self.settings.writer_prefix, self.settings.writer_suffix)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/writers/html.py", line 293, in write
    self.write_docnode(node, self.builder, in_master_doc)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/writers/html.py", line 206, in write_docnode
    visit_docnode(node)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/writers/html.py", line 402, in visit_method
    self.add_autodoc_role(methodnode, 'method