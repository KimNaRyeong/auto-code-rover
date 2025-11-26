Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import setup

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

def reproduce_issue():
    # Create a temporary directory for the documentation
    doc_dir = 'doc_tmp'
    os.makedirs(doc_dir, exist_ok=True)

    # Configure Sphinx
    conf_py = os.path.join(doc_dir, 'conf.py')
    with open(conf_py, 'w') as f:
        f.write("autodoc_typehints = 'none'\n")

    # Create a sample module with a class and a property
    module_py = os.path.join(doc_dir, 'module.py')
    with open(module_py, 'w') as f:
        f.write("class MyClass:\n"
               "    @property\n"
               "    def my_property(self) -> str:\n"
               "        return 'hello'\n")

    # Run Sphinx
    app = Sphinx(doc_dir, doc_dir, doc_dir, doc_dir)
    setup(app)

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise

    # Check if the type hint is still present in the output
    html_file = os.path.join(doc_dir, '_build', 'html', 'module.html')
    with open(html_file) as f:
        content = f.read()
        if '-> str' in content:
            raise AssertionError("Type hint is still present in the output")

if __name__ == '__main__':
    reproduce_issue()
```
This script creates a temporary directory for the documentation, configures Sphinx to use `autodoc_typehints = 'none'`, creates a sample module with a class and a property, runs Sphinx, and checks if the type hint is still present in the output. If it is, an `AssertionError` is raised with a stack trace of the issue.