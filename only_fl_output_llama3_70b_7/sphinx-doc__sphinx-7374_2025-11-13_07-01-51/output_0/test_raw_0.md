Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder

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

try:
    # Create a Sphinx project
    project_dir = 'project'
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, 'conf.py'), 'w') as f:
        f.write("extensions = ['sphinx.ext.autodoc']\n")
    
    # Create a Python module with a function containing underscores
    module_dir = os.path.join(project_dir, 'modules')
    os.makedirs(module_dir, exist_ok=True)
    with open(os.path.join(module_dir, '__init__.py'), 'w') as f:
        pass
    with open(os.path.join(module_dir, 'example.py'), 'w') as f:
        f.write("def example_python_function(foo):\n    pass\n")
    
    # Build the HTML documentation
    app = Sphinx(project_dir, project_dir, os.path.join(project_dir, '_build'), os.path.join(project_dir, '_build'))
    app.builder = StandaloneHTMLBuilder(app)
    app.build()
    
    # Check if the anchor is correct
    with open(os.path.join(project_dir, '_build', 'html', 'modules', 'example.html')) as f:
        html_content = f.read()
        assert '#example_python_function' in html_content, "Anchor is not using underscores"
    
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script creates a Sphinx project with a Python module containing a function with underscores, builds the HTML documentation, and checks if the anchor is correct. If the anchor is not using underscores (i.e., it's using dashes), an `AssertionError` is raised, and the script prints a stack trace of the issue and exits with code 1. If the anchor is correct, the script exits with code 0.