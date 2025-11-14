Here is the reproducer script:

```python
import sys
from docutils import nodes, utils

def test():
    """test tests something.
    .. default-role:: cmsreference
    """
    pass

try:
    trim_docstring(nodes.Heading("heading", "heading"), ["test()"])
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected no exception")

sys.exit(0)
```

This script defines a test function with a docstring that starts at the first line, which should trigger the issue. It then attempts to call `trim_docstring` with this docstring and an empty list of lines (since we're only interested in reproducing the error). If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.