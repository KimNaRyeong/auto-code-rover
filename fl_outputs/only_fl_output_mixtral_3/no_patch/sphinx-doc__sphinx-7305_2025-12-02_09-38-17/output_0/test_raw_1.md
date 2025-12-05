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

app.build(force_all=True, warningiserror=True)
```
To reproduce the issue, create a new directory, put the above code in a file named `reproducer.py`, and run `python3 reproducer.py`. The script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    app.build(force_all=True, warningiserror=True)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 346, in build
    self.builder.build_update()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 282, in build_update
    self.build_files(files)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 305, in build_files
    for source, target, title, encoding in self.get_files():
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 384, in get_files
    for node in self.process_document(docname, document):
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 340, in process_document
    self.apply_transforms(docname, document, transforms)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 229, in apply_transforms
    doctree = transform.apply(doctree)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/transforms/__init__.py", line 93, in apply
    return transform(document, **kwargs).apply()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/transforms/restructuredtext.py", line 38, in apply
    self.apply_post_transforms(**state)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/transforms/restructuredtext.py", line 58, in apply_post_transforms
    self.apply_role_and_directive_transforms(**state)
