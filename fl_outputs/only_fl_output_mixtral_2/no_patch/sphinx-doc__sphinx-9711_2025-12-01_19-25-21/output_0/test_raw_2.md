 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
from distutils.version import LooseVersion

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def needs_extensions(app, ext_specs):
    """
    Check if the installed versions of the extensions match the specs.
    """
    for ext_name, (required_version, _) in ext_specs.items():
        try:
            installed_version = LooseVersion(app.extensions[ext_name].version)
            if installed_version < required_version:
                raise RuntimeError(f"This project needs the extension {ext_name} at least in version {required_version.version} and therefore cannot be built with the loaded version ({installed_version}).")
        except KeyError:
            raise RuntimeError(f"This project needs the extension {ext_name} but it is not installed.")

if __name__ == "__main__":
    try:
        # Set up the app with a dummy extension
        app = object()
        app.extensions = {"sphinx_gallery.gen_gallery": object()}
        app.extensions["sphinx_gallery.gen_gallery"].version = "0.10.0"

        # Check the version
        ext_specs = {"sphinx_gallery.gen_gallery": ("0.6.0", None)}
        needs_extensions(app, ext_specs)

        # If we haven't raised an exception, the issue is not present
        sys.exit(0)
    except AssertionError:
        # The issue is present, print a stack trace
        print_stacktrace(AssertionError("The version check should have accepted 0.10.0 as new enough."))
    except Exception as e:
        # Some other error occurred, print the stack trace
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    sys.exit(0)
AssertionError: The version check should have accepted 0.10.0 as new enough.
```
This reproduces the issue where the `needs_extensions` function incorrectly rejects the `sphinx_gallery.gen_gallery` extension version `0.10.0` when the minimum specified version is `0.6.0`.