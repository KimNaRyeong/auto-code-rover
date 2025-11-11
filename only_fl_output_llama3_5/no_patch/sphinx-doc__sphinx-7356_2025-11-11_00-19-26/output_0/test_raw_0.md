Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive

def setup_sphinx():
    sphinx.domains.python.setup()

def test_python_domain_ids():
    setup_sphinx()
    rst = """
.. py:function:: example_python_function(foo)

    Some function.
"""
    from io import StringIO
    from docutils.core import publish_string
    
    output = publish_string(rst, writer_name='html')
    
    if "example-python-function" in output.decode('utf-8'):
        raise AssertionError("Expected 'example_python_function' but got 'example-python-function'")

if __name__ == "__main__":
    try:
        test_python_domain_ids()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up the Sphinx domain for Python, then uses the `publish_string` function to process a piece of RST that defines a Python function. It checks if the generated HTML contains the expected fragment identifier (`#example_python_function`) or the new one (`#example-python-function`). If it finds the new one, it raises an `AssertionError`.