Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
        app.extensions.append("sphinx_gallery.gen_gallery")
        app.config.sphinx_gallery_version = "0.10.0"
        assert needs_extensions_check(app.config.sphinx_gallery_version)
        print("Version 0.10.0 is accepted as it meets the minimum version requirement of 0.6.0")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Version 0.10.0 is not accepted, but it should be")

if __name__ == "__main__":
    main()
```
<|start_header_id|>