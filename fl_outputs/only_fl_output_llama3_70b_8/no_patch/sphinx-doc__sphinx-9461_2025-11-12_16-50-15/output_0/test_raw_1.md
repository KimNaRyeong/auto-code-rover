Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.cmd.build import main as sphinx_build
import subprocess

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

class BaseClass:
    @classmethod
    @property
    def baseclass_class_property(cls):
        """Some class property."""
        return "property"

def test_documentation():
    src_dir = os.path.dirname(__file__)
    out_dir = os.path.join(src_dir, "_build", "html")
    conf_py = os.path.join(src_dir, "conf.py")

    with open(conf_py, "w") as f:
        f.write("extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary']\n")
        f.write("autosummary_generate = True\n")

    subprocess.check_call(["sphinx-apidoc", "-o", out_dir, src_dir])

    with open(os.path.join(out_dir, "modules", "reproducer.html"), "r") as f:
        html_content = f.read()
    
    assert "baseclass_class_property" in html_content, "Method not documented"
    print("Issue is fixed!")

if __name__ == "__main__":
    try:
        test_documentation()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script defines a class `BaseClass` with a method decorated with both `@classmethod` and `@property`. It then uses Sphinx to generate HTML documentation for this class. The script checks if the generated HTML content contains the method's name, and raises an `AssertionError` if it doesn't. If the issue is present, the script prints a stack trace of the error and exits with code 1. If the issue is fixed, the script prints a success message and exits with code 0.

Please note that this script assumes that Sphinx is installed and available in the system's PATH.