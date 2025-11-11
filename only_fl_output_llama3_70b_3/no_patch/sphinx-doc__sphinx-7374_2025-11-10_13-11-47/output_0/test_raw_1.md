Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.directives import Directive
from sphinx.domains.python import PyFunction

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

def test_python_domain_ids():
    class MyDirective(Directive):
        has_content = False
        required_arguments = 1
        optional_arguments = 0

        def run(self):
            env = self.state.document.settings.env
            domain = env.get_domain('py')
            funcname = self.arguments[0]
            anchor = domain.get_object-anchor(funcname)
            if '-' in anchor:
                raise AssertionError("Python domain IDs are using dashes instead of underscores")
            return []

directives.register_directive('mydir', MyDirective)

try:
    with open('test.rst', 'w') as f:
        f.write(".. mydir:: example_python_function\n")
    with open('conf.py', 'w') as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    os.system("sphinx-build -b html . _build")
    with open(os.path.join("_build", "index.html"), "r") as f:
        html_content = f.read()
        if "#example-python-function" in html_content:
            raise AssertionError("Python domain IDs are using dashes instead of underscores")
except Exception as e:
    print_stacktrace(e)
    raise

if __name__ == "__main__":
    test_python_domain_ids()
```
This script creates a custom directive, uses it to generate an RST file, builds the HTML documentation with Sphinx, and checks if the generated HTML file contains the expected anchor ID `#example_python_function` instead of `#example-python-function`. If it finds the latter, it raises an `AssertionError` with a stack trace.