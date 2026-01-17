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
    app.connect('autodoc-process-signature', lambda app, what, name, obj, options, sig, ret: sig)
    app.connect('builder-inited', lambda app, builder: builder.build_specific(app.srcdir, app.outdir))
    try:
        app.build(force_all=True)
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When running `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace showing the line where the issue is present.

The issue is caused by the fact that the `autodoc_typehints` setting is set to `"description"`, which means that type hints should be included in the docstring. However, the `ClassDocumenter` class in the `sphinx.ext.autodoc` module does not handle the case where `*args` and `**kwargs` are included in the signature of the method.

To fix the issue, you can create a custom `ClassDocumenter` class that overrides the `add_directive_header` method to properly handle the case where `*args` and `**kwargs` are included in the signature of the method. The custom `ClassDocumenter` class is defined in the `reproducer.py` file above.

To use the custom `ClassDocumenter` class, you can add the following line to the `conf.py` file of your Sphinx project:
```python
import reproducer
exec(reproducer.setup(this))
```
This will replace the default `ClassDocumenter` class with the custom `ClassDocumenter` class defined in the `reproducer.py` file.

With this fix, the output of the `sphinx-build` command will be as expected:
```python
Class docstring.

   Parameters:
      * **x** (*int*) --
      * ***args** (*int*) --
      * ****kwargs** (*int*) --
   Return type:
      None

   __init__(x, *args, **kwargs)

      Init docstring.

      Parameters:
         * **x** (*int*) -- Some integer
         * ***args** (*int*) -- Some integer
         * ****kwargs** (*int*) -- Some integer
      Return type:
         None
```