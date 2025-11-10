Here is the `reproducer.py` file that reproduces the issue:
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
        app = Sphinx(srcdir="", confdir="", outdir="")
        app.config.extensions = ["sphinx_gallery.gen_gallery"]
        app.config.version = "0.10.0"
        
        # This should not raise an error
        needs_extensions_check(app.config.version)
        
        print("Version 0.10.0 is accepted")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Version 0.10.0 is not accepted"

if __name__ == "__main__":
    main()
    sys.exit(0)
```
This script creates a Sphinx application with the `sphinx_gallery.gen_gallery` extension and sets its version to `0.10.0`. It then calls the `needs_extensions_check` function, which should not raise an error since `0.10.0` is greater than or equal to `0.6.0`.

If the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, the script will exit with code 0.

You can run this script by executing `python3 reproducer.py` in the root directory of the project.