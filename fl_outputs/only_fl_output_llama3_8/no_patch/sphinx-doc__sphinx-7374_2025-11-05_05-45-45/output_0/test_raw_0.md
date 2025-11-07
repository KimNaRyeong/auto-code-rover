Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive

def setup_sphinx():
    sphinx.domains.python.setup()

def test_python_domain_ids():
    setup_sphinx()
    rst = '.. py:function:: example_python_function(foo)\n' \
         '    Some function.\n'
    from io import StringIO
    from docutils.core import publish_string
    output = StringIO()
    publish_string(rst, writer_name='html', outputfile=output)
    if '#example-python-function' in output.getvalue():
        raise AssertionError('Expected "#example_python_function" but got "#example-python-function"')

def main():
    try:
        test_python_domain_ids()
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```

This script sets up the Sphinx domain for Python, then attempts to publish an RST document that defines a Python function with underscores in its name. If the published output contains dashes instead of underscores, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace when the error occurs.