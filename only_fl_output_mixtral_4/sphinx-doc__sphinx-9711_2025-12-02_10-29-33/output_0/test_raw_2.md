 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import sphinx
from sphinx.application import Sphinx

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_version():
    app = Sphinx(sys.argv[1:], io=None, warningiserror=True)
    app.setup_extension('sphinx_gallery.gen_gallery')
    app.check_extensions_version()

if __name__ == '__main__':
    try:
        check_version()
    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception occurred while checking the version"
```
To reproduce the issue, run the script with the path to the `doc` directory as the argument:
```bash
$ python3 reproducer.py path/to/mplcursors/doc
```
This will raise an `AssertionError` with a stack trace, indicating that the version of `sphinx_gallery` is not new enough.

To fix the issue, either downgrade `sphinx-gallery` to version 0.9 or higher, or modify the `needs_extensions` check in the `conf.py` file to accept version 0.10 of `sphinx_gallery`.