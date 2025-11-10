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

def test_python_domain_ids():
    src_dir = 'docs'
    out_dir = 'build'
    builder = StandaloneHTMLBuilder(Sphinx(src_dir, out_dir, 'index'))
    
    rst_content = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    
    with open(os.path.join(src_dir, 'test.rst'), 'w') as f:
        f.write(rst_content)
    
    builder.build_all()
    
    with open(os.path.join(out_dir, 'index.html')) as f:
        html_content = f.read()
    
    if '#example-python-function' in html_content:
        raise AssertionError("Python domain IDs are using dashes instead of underscores")
    else:
        print("Issue is fixed")

if __name__ == '__main__':
    try:
        test_python_domain_ids()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a minimal Sphinx project, writes an RST file with a Python function definition, builds the HTML documentation using Sphinx, and checks if the generated HTML contains the expected anchor ID. If it does, it raises an `AssertionError` with a stack trace. If not, it prints a success message and exits with code 0.