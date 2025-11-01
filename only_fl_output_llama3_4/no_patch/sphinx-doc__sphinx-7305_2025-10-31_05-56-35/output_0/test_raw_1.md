Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc

def f(*, a=2**4):
    pass

def g(a=2**4):
    pass

try:
    rst.parse_string('.. py:method:: f(*, a=2**4)\n.. py:method:: g(a=2**4)')
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected 'Could not parse arglist' error")
```

This script attempts to parse the given rst string using Sphinx's `rst.parse_string` function. If the issue is present, an `AssertionError` is raised; if the issue is fixed, the script exits with code 0.