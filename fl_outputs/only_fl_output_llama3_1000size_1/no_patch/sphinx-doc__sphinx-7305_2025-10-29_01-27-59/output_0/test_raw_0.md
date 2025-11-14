Here is the reproducer script:

```python
import sphinx
from sphinx.ext import autodoc

def f(*, a=2**4):
    pass

def g(a=2**4):
    pass

try:
    autodoc.autodoc(f)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")

try:
    autodoc.autodoc(g)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script attempts to generate documentation for the `f` and `g` functions using Sphinx's autodoc extension. If an error occurs during this process, it prints a stack trace and raises an `AssertionError`.