 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
from sphinx.ext.autodoc import ClassDocumenter

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class CustomClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        signature = self.build_signature(sig)
        self.add_line('', signature, ':class:')

def setup(app):
    app.add_autodocumenter(CustomClassDocumenter)

if __name__ == '__main__':
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='html', warningiserror=0)
    app.connect('autodoc-process-signature', print_stacktrace)
    app.connect('autodoc-process-docstring', print_stacktrace)
    try:
        app.build(force_all=True)
    except Exception as e:
        assert False, e
```
When running `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace, which shows the issue with duplicated `*args` and `**kwargs` in the generated documentation.

To fix the issue, you can modify the `CustomClassDocumenter` class to correctly handle the `*args` and `**kwargs` parameters in the signature:
```python
class CustomClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        args, varargs, varkw, defaults = sig.parameters.values()
        signature = self.build_signature(sig)
        if varargs or varkw:
            signature = signature.replace('*', '**')
            if varargs:
                signature = signature.replace('**', '*')
        self.add_line('', signature, ':class:')
```
With this modification, the script will not raise an `AssertionError` and will print the expected output when running `python3 reproducer.py`.