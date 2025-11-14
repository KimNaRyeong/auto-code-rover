Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from sphinx.application import Sphinx

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
    src_dir = os.path.dirname(__file__)
    out_dir = os.path.join(src_dir, '_build')
    app = Sphinx(src_dir, src_dir, out_dir, out_dir, 'html')

    rst_content = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write(rst_content)

    app.build()

    html_file = os.path.join(out_dir, 'index.html')
    with open(html_file, 'r') as f:
        html_content = f.read()
        if '#example-python-function' in html_content:
            raise AssertionError("Python domain IDs are broken")
        elif '#example_python_function' not in html_content:
            print("Issue is fixed")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
```
This script creates a minimal Sphinx project, builds it, and checks the generated HTML file for the expected anchor ID. If the issue is present, it raises an `AssertionError` with a stack trace. If the issue is fixed, it prints a success message and exits with code 0.