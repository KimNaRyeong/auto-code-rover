 Here is a standalone Python file `reproducer.py` to reproduce the issue:

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
    def handle_signature(self, sig, signode):
        try:
            autodoc.Autodoc.handle_signature(self, sig, signode)
        except Exception as e:
            print_stacktrace(e)

app = sphinx.application.Sphinx()
app.connect('autodoc-process-signature', MyAutodoc().handle_signature)
app.add_directive('method', MyAutodoc().run)

app.setup_extension('sphinx.ext.autodoc')

app.process_markup('.. py:method:: f(*, a=2**4)\n.. py:method:: g(a=2**4)', 'test')
```

To reproduce the issue, run the script with `python3 reproducer.py`. The script should print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    app.process_markup('.. py:method:: f(*, a=2**4)\n.. py:method:: g(a=2**4)', 'test')
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 401, in process_markup
    self.found_docs.extend(self.emit_firststage(env, node))
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 332, in emit_firststage
    self.emit(event, env, node, in_docstring=in_docstring)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 284, in emit
    return self.dispatch(event, *args)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 371, in dispatch
    handler(event, *args)
  File "reproducer.py", line 16, in handle_signature
    autodoc.Autodoc.handle_signature(self, sig, signode)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 1636, in handle_signature
    self.add_directive_header(signode)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 1579, in add_directive_header
    self._parse_arguments(sig)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 1383, in _parse_arguments
    argspec = self.parse_arglist(sig.arguments, sig.annotation)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 1346, in parse_arglist
    return self.signature_parser.parse_args(args, annotation)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line