Certainly! Below is a standalone Python script named `reproducer.py` designed to reproduce the issue as described. When executed in the root directory of a Sphinx project, it will document the `Thing` class and check for the correct default values on its `__init__` method. If the issue is present, it will print a stack trace and raise an `AssertionError`. Otherwise, it will exit with code `0`, indicating the issue is fixed.

```python
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_documenter():
    from sphinx.application import Sphinx
    from sphinx.ext.autodoc import ModuleDocumenter, Documenter
    from io import StringIO

    # Create a dummy Sphinx application object
    app = Sphinx(
        srcdir='.',      # Current directory as source
        confdir='.',     # Use current directory for conf.py
        outdir='./_build',   # Use _build directory for output
        doctreedir='./_doctree',
        buildername='html'  # HTML builder
    )
    app.setup_extension('sphinx.ext.autodoc')
    app.config.autodoc_preserve_defaults = True

    # Create a fake output buffer and Documenter
    output = StringIO()
    doc = Documenter(app, 'module', 'reproducer', analyzer=None, writer=None)
    doc.options.members = ['Thing']
    doc.options.undoc_members = True
    doc.options.show_inheritance = True
    doc.generate(more_content=None, real_modname=None, check_module=False)

    output_value = output.getvalue()
    if "kw_with_default='Foo'" not in output_value:
        raise AssertionError("Default values are not correctly documented.")

try:
    test_documenter()
    print("Issue seems fixed.")
except Exception as e:
    print_stacktrace(e)
    raise
```

Note: This script assumes that the Sphinx project is correctly set up in the current directory and that `reproducer.py` and your class definition (`Thing` in this case) are correctly accessible to Sphinx. You may need to adjust the paths or setup according to your project's structure.

To ensure this script works as intended, please make sure your Sphinx project's `conf.py` is configured to find and document the `Thing` class, and that Sphinx, as well as other necessary dependencies, are correctly installed in your environment.