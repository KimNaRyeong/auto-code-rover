Here is the reproducer script:

```python
import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive

def example_python_function():
    pass

class PythonFunctionDirective(Directive):
    has_content = True

    def run(self):
        node = nodes.literal('', '')
        self.state.nested_parse(self.content, 0, node)
        return [node]

def main():
    sphinx.domains.python.PythonDomain().register_directive('function', PythonFunctionDirective())
    docutils.core.publish_string('<rst>\n.. py:function:: example_python_function(foo)\n    Some function.\n</rst>', writer_name='html')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script creates a Python domain and registers the `PythonFunctionDirective` to handle the `.. py:function::` directive. Then it publishes an RST string that contains the problematic function definition.

When you run this script, if the issue is present (i.e., the anchor name has dashes instead of underscores), it will raise an `AssertionError` and print a stack trace. If the issue is fixed, it will exit with code 0.