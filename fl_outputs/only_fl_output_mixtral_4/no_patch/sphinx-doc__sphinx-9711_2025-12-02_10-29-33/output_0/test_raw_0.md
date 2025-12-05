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
    app.connect('config-inited', lambda app, config: config.init_version('sphinx_gallery.gen_gallery', '0.6.0'))
    app.connect('config-inited', lambda app, config: assert app.check_dependencies() is None)

if __name__ == '__main__':
    try:
        check_version()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with the path to the `doc` directory as the argument:
```
$ python3 reproducer.py path/to/mplcursors/doc
```
This will raise an `AssertionError` with a stack trace, indicating that the version of `sphinx_gallery.gen_gallery` is not new enough.

To fix the issue, update the version check in the `needs_extensions` check to compare versions as tuples instead of strings. This can be done by modifying the `check_dependencies` method in the `sphinx.ext.compat rev` module:
```python
def check_dependencies(self):
    """Check the versions of all needed extensions."""
    for ext, minver in self.config.needs_extensions.items():
        try:
            ver = pkg_resources.get_distribution(ext).version
        except pkg_resources.DistributionNotFound:
            raise ExtensionError(f"Can't find extension: {ext}")
        if version_tuple(ver) < version_tuple(minver):
            return ExtensionError(f"This project needs the extension {ext} at least in version {minver} and therefore cannot be built with the loaded version ({ver}).")
    return None
```
With this modification, the version check will correctly compare versions as tuples, allowing the build to proceed with the current version of `sphinx_gallery.gen_gallery`.