Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from sphinx.ext import inheritance_diagram
from sphinx.application import SphinxApplication
import os
import sys

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
    app = SphinxApplication()
    app.builder = sphinx.builders.get_builder('html')
    app.config.inheritance_diagram_module_name_prefix = 'my_package'
    app.config.inheritance_diagram_file_suffix = '.html'

    try:
        os.makedirs('docs_source', exist_ok=True)
        with open(os.path.join('docs_source', '__init__.py'), 'w') as f:
            pass

        with open(os.path.join('docs_source', 'my_package', '__init__.py'), 'w') as f:
            pass

        with open(os.path.join('docs_source', 'my_package', 'my_class_1.py'), 'w') as f:
            f.write("class my_package.MyClass1: pass\n")

        with open(os.path.join('docs_source', 'my_package', 'my_class_2.py'), 'w') as f:
            f.write("class my_package.MyClass2: pass\n")

        app.build()

        if not os.path.exists('docs_build'):
            raise AssertionError("Expected 'docs_build' directory to be created")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_issue()
```

This script creates a minimal Sphinx project with the necessary files and directories, builds it using `sphinx-build`, and checks if the expected output is generated. If an error occurs during the build process or if the expected output is not generated, it prints the stack trace and exits with code 1.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it using `python3 reproducer.py`.