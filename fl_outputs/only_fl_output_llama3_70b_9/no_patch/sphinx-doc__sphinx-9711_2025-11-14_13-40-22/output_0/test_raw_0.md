Here is the `reproducer.py` script to reproduce the issue:
```
import sys
from sphinx.application import Sphinx

def needs_extensions_check(version):
    return version >= "0.6.0"

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

def main():
    try:
        app = Sphinx(srcdir="", confdir="")
        app.extensions = ["sphinx_gallery.gen_gallery"]
        app.config.extensions["sphinx_gallery.gen_gallery"] = "0.10.0"
        
        # This should not raise an error
        assert needs_extensions_check("0.10.0"), f"Version 0.10.0 is not new enough"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script creates a Sphinx application, sets up the `sphinx_gallery.gen_gallery` extension with version `0.10.0`, and then calls the `needs_extensions_check` function to verify that the version is new enough. If the check fails, it raises an `AssertionError` and prints the stack trace using the provided `print_stacktrace` function.

To run this script, save it as `reproducer.py` in the root directory of the project and execute it with `python3 reproducer.py`.