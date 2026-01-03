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

class PatchedClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        super().add_directive_header(sig)
        if self.options.get('autodoc_typehints') == 'description':
            for line in sig.split('\n'):
                if line.startswith(':param '):
                    param_name = line[7:].split(':')[0].strip()
                    param_type = line[7:].split(':')[1].strip()[1:-1]
                    if '<' in param_type:
                        param_type_name = param_type.split('<')[0].strip()
                        link = f'<{sphinx.application.CONFIG.intersphinx_mapping["python"]["base_url"]}/{param_type_name}>'
                        self.add_line(f':type {param_name}: {link}', '   ')

def setup(app):
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-signature', lambda sig, sig_and_returns, object, options, lines: PatchedClassDocumenter.add_directive_header(PatchedClassDocumenter(app, object, 'class', sig, sig_and_returns, options, lines)))

def test():
    try:
        app = sphinx.application.Sphinx(srcdir='.')
        app.build(force_all=True, doctree_dir=None)
    except Exception as e:
        print_stacktrace(e)
        assert False
    else:
        assert True

if __name__ == '__main__':
    test()
```
The script uses the `sphinx.application.Sphinx` class to create a Sphinx application object and builds the documentation. The `PatchedClassDocumenter` class is a subclass of the `sphinx.ext.autodoc.ClassDocumenter` class, which adds a type link for parametrized types in the parameter description. The `setup` function sets up the `PatchedClassDocumenter` class as the new `ClassDocumenter` class for the Sphinx application object. The `test` function runs the Sphinx build process and checks for any exceptions. If an exception is raised, the script prints the stack trace and raises an `AssertionError`. If no exceptions are raised, the script exits with code 0.

To reproduce the issue, run the script with `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace.

To fix the issue, modify the `PatchedClassDocumenter` class to correctly extract the parametrized type name. For example, the following code should work:
```python
class PatchedClassDocumenter(ClassDocumenter):
    def add_directive_header(self, sig):
        super().add_directive_header(sig)
        if self.options.get('autodoc_typehints') == 'description':
            for line in sig.split('\n'):
                if line.startswith(':param '):
                    param_name = line[7:].split(':')[0].strip()
                    param_type = line[7:].split(':')[1].strip()[1:-1]
                    if '<' in param_type:
                        param_type_name = param_type.split('<')[1].split('>')[0].strip()
